from HandRecognitionModule import HandRecognition
import pyautogui as ag
import cv2 as cv
from math import sqrt


def dist(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


webcam = cv.VideoCapture(0)
hand_rec = HandRecognition()
while webcam.isOpened():
    success, frame = webcam.read()
    frame = cv.flip(frame, 1)
    if not success:
        print("Unable to read video frame")
        continue
    data_points, frame = hand_rec.detect_hands(frame, print_image=False, flip_image=False)
    # print(data_points)

    if data_points:
        first_hand = data_points[0]
    else:
        continue

    # Draw guidelines
    image_height, image_width, _ = frame.shape
    index_finger = first_hand[8][:2]
    index_finger = [image_width * index_finger[0], image_height * index_finger[1]]
    print(index_finger)
    primary_color = (255, 0, 0)
    secondary_color = (0, 255, 0)
    accent_color = (0, 0, 255)
    thickness = 2
    # Draw two circles
    center = (image_width // 2, image_height // 2)
    inside_color = outside_color = primary_color
    if dist(index_finger, center) < 50:
        inside_color = secondary_color
    elif dist(index_finger, center) < 150:
        outside_color = secondary_color

    cv.circle(frame, (image_width // 2, image_height // 2), 50, inside_color, thickness=thickness)
    cv.circle(frame, (image_width // 2, image_height // 2), 150, outside_color, thickness=thickness)

    # cv.line(frame, (image_width // 2 - 50, image_height // 2), (image_width // 2 + 50, image_height // 2),
    #         primary_color, thickness=thickness)
    # cv.line(frame, (image_width // 2, image_height // 2 - 50), (image_width // 2, image_height // 2 + 50),
    #         primary_color, thickness=thickness)

    cv.imshow("Visual Mouse", frame)
    cv.waitKey(1)
