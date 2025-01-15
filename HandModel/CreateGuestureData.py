import cv2
import pygame
import mediapipe as mp
import csv
import os

def save_landmarks_to_csv(hand_landmarks, gesture_label, filename):
    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            header = ['gesture_label'] + [f'landmark_{i}_{axis}' for i in range(21) for axis in ('x', 'y', 'z')]
            writer.writerow(header)

    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        row = [gesture_label] + [coord for landmark in hand_landmarks.landmark for coord in (landmark.x, landmark.y, landmark.z)]
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

    frame = cv2.flip(frame, 1)

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

            keys = pygame.key.get_pressed() #have to press u to register thumbs up, d for thumbs down, and b everything else

            if keys[pygame.K_u]:
                save_landmarks_to_csv(hand_landmarks, "Thumbs Up", "HandModel/thumbs_up_data.csv")
                cv2.putText(frame, "Thumbs Up", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif keys[pygame.K_d]:
                save_landmarks_to_csv(hand_landmarks, "Thumbs Down", "HandModel/thumbs_down_data.csv")
                cv2.putText(frame, "Thumbs Down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif keys[pygame.K_b]:
                save_landmarks_to_csv(hand_landmarks, "Blank", "HandModel/blank_data.csv")
                cv2.putText(frame, "Blank", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Hand Gesture Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

pygame.quit()
cap.release()
cv2.destroyAllWindows()