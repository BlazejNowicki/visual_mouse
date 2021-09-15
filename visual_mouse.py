from cv2 import data
from HandRecognitionModule import HandRecognition
import pyautogui
import cv2 as cv
import math
from enum import Enum


class Color(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)


class Thickness(Enum):
    THIN = 2
    THICK = 4


class MouseControl():
    def __init__(self):
        self.left_button_clicked = False
        self.media_control_mode = False
        self.inside_radious = 70
        self.outside_radious = 200
        self.frame_width = None
        self.frame_height = None

    def identify_gesture(self, data_points):
        # check if all finger are curled (media control mode)
        finger_ids = [(6,9),(10,12),(14,16),(18,20)]
        wrist_id = 0
        for tip_id, mcp_id in finger_ids:
            mcp_dist = self.dist(data_points[mcp_id],
                                 data_points[wrist_id])
            tip_dist = self.dist(data_points[tip_id],
                                 data_points[wrist_id])
            if mcp_dist < tip_dist:
                return False
        return True

    def operate(self, data_points,  frame):
        # main function, that responds to user's actions
        self.frame_height, self.frame_width, _ = frame.shape
        index_figer = data_points[8]  # in [0,1] scale

        self.media_control_mode = self.identify_gesture(data_points)
        # print(self.media_control_mode)
        if not self.media_control_mode:
            self.add_graphics_normal(frame, index_figer)
            self.move_mouse(data_points)
        else:
            self.add_graphics_media(frame, index_figer)
            self.control_media(data_points)

    def scale_to_pixels(self, x):
        return [self.frame_width*x[0], self.frame_height*x[1]]

    def move_mouse(self, data_points):
        index_knuckle = self.scale_to_pixels(data_points[5])
        index_tip = self.scale_to_pixels(data_points[8])
        middle_tip = self.scale_to_pixels(data_points[12])
        center = (self.frame_width//2, self.frame_height//2)

        index_finger_in_center = False
        index_finger_in_outer_circle = False
        if self.dist(index_tip, center) < self.inside_radious:
            index_finger_in_center = True
        if self.dist(index_tip, center) < self.outside_radious:
            index_finger_in_outer_circle = True

        left_click_flag = self.dist(middle_tip, index_knuckle) < self.dist(
            middle_tip, index_tip) and index_finger_in_center

        if left_click_flag and not self.left_button_clicked:
            self.left_button_clicked = True
            pyautogui.leftClick()
            print("left-click")
        elif not left_click_flag and self.left_button_clicked:
            left_click = False

        # Moving mouse around
        if index_finger_in_outer_circle:
            move_horizontally = (index_tip[0] - self.frame_width//2)
            move_vertically = (index_tip[1] - self.frame_height//2)
            move_horizontally = 20 * ((move_horizontally)/150)**3
            move_vertically = 20 * ((move_vertically)/150)**3
            pyautogui.move(move_horizontally, move_vertically, _pause=False)

    def control_media(self, data_points):
        pass

    def add_graphics_media(self, frame, index_figer):
        pass

    def dist(self, a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    def add_graphics_normal(self, frame, index_finger):
        # change scale from [0, 1] to pixels
        index_finger = [self.frame_width * index_finger[0],
                        self.frame_height * index_finger[1]]
        center = (self.frame_width // 2, self.frame_height // 2)

        # draw guidelines
        inside_color = outside_color = Color.GREEN.value

        index_finger_in_center = False
        index_finger_in_outer_circle = False
        if self.dist(index_finger, center) < self.inside_radious:
            inside_color = Color.RED.value
            index_finger_in_center = True
        if self.dist(index_finger, center) < self.outside_radious:
            outside_color = Color.RED.value
            index_finger_in_outer_circle = True

        cv.circle(img=frame,
                  center=(self.frame_width//2, self.frame_height//2),
                  radius=self.inside_radious,
                  color=inside_color,
                  thickness=Thickness.THIN.value)

        cv.circle(img=frame,
                  center=(self.frame_width//2, self.frame_height//2),
                  radius=self.outside_radious,
                  color=outside_color,
                  thickness=Thickness.THIN.value)


def main():
    webcam = cv.VideoCapture(0)
    hand_rec = HandRecognition()
    mouse_ctrl = MouseControl()
    while webcam.isOpened():
        success, frame = webcam.read()
        if not success:
            print('Unable to read the frame')
            continue
        hand_landmarks, frame = hand_rec.detect_hands(
            frame, print_image=False, one_hand_only=True)

        if hand_landmarks:
            mouse_ctrl.operate(hand_landmarks, frame)

        cv.imshow("Visual Mouse", frame)
        cv.waitKey(1)


if __name__ == '__main__':
    main()
