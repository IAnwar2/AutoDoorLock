import face_recognition
import cv2
import numpy as np
import os
import glob
from tensorflow.keras.models import load_model
import mediapipe as mp
import time


main_folder_path = 'FacePics'
loggedInUser=""
safeStatus = "locked"


def startRecognition():
    global safeStatus
    unlocked = False

    video_capture = cv2.VideoCapture(0)

    #make array of sample pictures with encodings
    known_face_encodings = []
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, main_folder_path, loggedInUser)

    #make an array of all the saved jpg files' paths
    list_of_files = glob.glob(os.path.join(path, '*.jpg'))
    number_files = len(list_of_files)

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    # Configure MediaPipe Hands
    hands = mp_hands.Hands(static_image_mode=False,
                max_num_hands=2,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5)

    # Load model for hand gesture recognition
    model = load_model("HandModel/hand_gesture_model.keras")

    for i in range(number_files):
        globals()['image_{}'.format(i)] = face_recognition.load_image_file(list_of_files[i])
        globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]
        known_face_encodings.append(globals()['image_encoding_{}'.format(i)])

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    last_prediction_time = 0  # Last time a prediction was made
    prediction_interval = 0.5  # Interval in seconds between predictions


    while True:
        ret, frame = video_capture.read() # Get a frame

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        frame = cv2.flip(frame, 1)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Hands
        result = hands.process(rgb_frame)

        # Process every other frame of video to save time
        if process_this_frame:

            # Check Face Recognition

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(small_frame)
            face_encodings = face_recognition.face_encodings(small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # Check if face is registered
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                if len(face_distances) > 0:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = loggedInUser
                        if unlocked == False:
                            unlocked = True

                face_names.append(name)

            # Check for guestures

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    current_time = time.time()
                    if current_time - last_prediction_time >= prediction_interval:

                        input_features = np.array([[landmark.x, landmark.y, landmark.z] for landmark in hand_landmarks.landmark]).flatten()
                        # Reshape the input to (1, 63)
                        input_features = input_features.reshape(1, -1)

                        # Predict the gesture
                        prediction = model.predict(input_features)
                        predicted_class = np.argmax(prediction) 
                        confidence = np.max(prediction)

                        gesture_labels = ["Blank", "Thumbs Down", "Thumbs Up"]  
                        gesture = gesture_labels[predicted_class]

                        # Display the predicted gesture and confidence
                        cv2.putText(frame, f"{gesture} ({confidence:.2f})", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        process_this_frame = not process_this_frame


        frame_width = frame.shape[1]  # Get the width of the frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Adjust for the horizontal flip of frame
            flipped_left = frame_width - right
            flipped_right = frame_width - left

            # Draw a box around the face
            cv2.rectangle(frame, (flipped_left, top), (flipped_right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (flipped_left, bottom - 35), (flipped_right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (flipped_left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'): # q to quit
            break

    video_capture.release()
    cv2.destroyAllWindows()