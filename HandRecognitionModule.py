import mediapipe as mp
import cv2 as cv


class HandRecognition:
    def __init__(self,
                 static_image_mode=False,
                 max_num_hands=1,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.drawing_styles = mp.solutions.drawing_styles
        self.hands = self.mp_hands.Hands(static_image_mode=static_image_mode,
                                         max_num_hands=max_num_hands,
                                         min_detection_confidence=min_detection_confidence,
                                         min_tracking_confidence=min_tracking_confidence)

    def detect_hands(self, img=None, print_image=True, flip_image=True):
        """Detects hands in image, returns list of lists of tuples, where hand[point[x,y,z]]"""
        output = []
        if img is not None:
            # Assuming that image is a 3 channel np bitmap in BGR format and that camera is front facing
            if flip_image:
                img = cv.cvtColor(cv.flip(img, 1), cv.COLOR_BGR2RGB)
            else:
                img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            img.flags.writeable = False  # according to doc it speeds things up
            results = self.hands.process(img)
            img.flags.writeable = True
            img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                        self.drawing_styles.get_default_hand_landmark_style(),
                        self.drawing_styles.get_default_hand_connection_style())
                    one_hand = []
                    for landmark in hand_landmarks.landmark:
                        one_hand.append((landmark.x, landmark.y, landmark.z))
                    output.append(one_hand)
            if print_image:
                cv.imshow('MediaPipe Hands', img)
        return output, img


# Example for reading hand position from default webcam
if __name__ == "__main__":
    cap = cv.VideoCapture(0)
    hand_rec = HandRecognition()
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        print(hand_rec.detect_hands(image))
        cv.waitKey(1)