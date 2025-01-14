import cv2
import pygame
import mediapipe as mp
import csv

def save_landmarks_to_csv(hand_landmarks, gesture_label, filename="HandModel/gesture_data.csv"):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        row = [gesture_label] + [coord for landmark in hand_landmarks.landmark 
                                 for coord in (landmark.x, landmark.y, landmark.z)]
        writer.writerow(row)

pygame.init()
screen = pygame.display.set_mode((500, 500))

# Initialize MediaPipe Hands and Drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Configure MediaPipe Hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=2,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a mirrored view
    frame = cv2.flip(frame, 1)

    # Convert the BGR frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cap.release()
                    pygame.quit()
                    cv2.destroyAllWindows()
                    exit()

            keys = pygame.key.get_pressed() #have to press u to register thumbs up and d to register thumbs down

            if keys[pygame.K_u]:
                save_landmarks_to_csv(hand_landmarks, "Thumbs Up")
                cv2.putText(frame, "Thumbs Up", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif keys[pygame.K_d]:
                save_landmarks_to_csv(hand_landmarks, "Thumbs Down")
                cv2.putText(frame, "Thumbs Down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                save_landmarks_to_csv(hand_landmarks, "Blank")
                cv2.putText(frame, "Blank", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame
    cv2.imshow("Hand Gesture Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

pygame.quit()
cap.release()
cv2.destroyAllWindows()