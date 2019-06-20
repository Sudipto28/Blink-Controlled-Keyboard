import cv2
import dlib
import numpy as np
from math import hypot

cap = cv2.VideoCapture(0)
board = np.zeros((100, 500), np.uint8)
board[:] = 255
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
font = cv2.FONT_HERSHEY_PLAIN

# Keyboard Settings
keyboard = np.zeros((400, 1000, 3), np.uint8)
keys_set_1 = {0: "Q", 1: "W", 2: "E", 3: "R", 4: "T", 5: "Y", 6: "U", 7: "I", 8: "O", 9: "P",
              10: "A", 11: "S", 12: "D", 13: "F", 14: "G", 15: "H", 16: "J", 17: "K", 18: "L",
              19: "Z", 20: "X", 21: "C", 22: "V", 23: "B", 24: "N", 25: "M", 26: ",", 27: "Space"
              }


def letter(letter_index, text, letter_light):
    width = 100
    height = 100
    thickness = 3

    # Keys
    if letter_index == 0:
        x = 0
        y = 0
    elif letter_index == 1:
        x = 100
        y = 0
    elif letter_index == 2:
        x = 200
        y = 0
    elif letter_index == 3:
        x = 300
        y = 0
    elif letter_index == 4:
        x = 400
        y = 0
    elif letter_index == 5:
        x = 500
        y = 0
    elif letter_index == 6:
        x = 600
        y = 0
    elif letter_index == 7:
        x = 700
        y = 0
    elif letter_index == 8:
        x = 800
        y = 0
    elif letter_index == 9:
        x = 900
        y = 0
    elif letter_index == 10:
        x = 50
        y = 100
    elif letter_index == 11:
        x = 150
        y = 100
    elif letter_index == 12:
        x = 250
        y = 100

    elif letter_index == 13:
        x = 350
        y = 100
    elif letter_index == 14:
        x = 450
        y = 100
    elif letter_index == 15:
        x = 550
        y = 100
    elif letter_index == 16:
        x = 650
        y = 100
    elif letter_index == 17:
        x = 750
        y = 100
    elif letter_index == 18:
        x = 850
        y = 100
    elif letter_index == 19:
        x = 100
        y = 200
    elif letter_index == 20:
        x = 200
        y = 200
    elif letter_index == 21:
        x = 300
        y = 200
    elif letter_index == 22:
        x = 400
        y = 200
    elif letter_index == 23:
        x = 500
        y = 200
    elif letter_index == 24:
        x = 600
        y = 200
    elif letter_index == 25:
        x = 700
        y = 200
    elif letter_index == 26:
        x = 800
        y = 200
    elif letter_index == 27:
        width = 500
        x = 250
        y = 300

    if letter_light == True:
        cv2.rectangle(keyboard, (x + thickness, y + thickness), (x + width - thickness, y + height - thickness),
                      (255, 255, 255), -1)
    else:
        cv2.rectangle(keyboard, (x + thickness, y + thickness), (x + width - thickness, y + height - thickness),
                      (255, 0, 0), thickness)

    # Text Settings
    font = cv2.FONT_HERSHEY_PLAIN
    font_scale = 5
    font_thickness = 2
    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
    width_text, height_text = text_size[0], text_size[1]
    text_x = int((width - width_text) / 2) + x
    text_y = int((height + height_text) / 2) + y
    cv2.putText(keyboard, text, (text_x, text_y), font, font_scale, (255, 0, 0), font_thickness)


def get_midpoint(p1, p2):
    x = int((p1.x + p2.x) / 2)
    y = int((p1.y + p2.y) / 2)
    return x, y


def get_blinking_ratio(eye_points, facial_landmarks):
    left = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    top = get_midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    bottom = get_midpoint(facial_landmarks.part(eye_points[4]), facial_landmarks.part(eye_points[5]))

    # hor_line = cv2.line(frame, left, right, (0, 255, 0), 1)
    # ver_line = cv2.line(frame, top, bottom, (0, 255, 0), 1)

    ver_line_length = hypot((top[0] - bottom[0]), (top[1] - bottom[1]))
    hor_line_length = hypot((left[0] - right[0]), (left[1] - right[1]))

    ratio = hor_line_length / ver_line_length

    return ratio


# Counters
frames = 0
letter_index = 0
blinking_frames = 0
text = ''

while True:
    _, frame = cap.read()
    # frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
    keyboard[:] = (0, 0, 0)
    frames += 1
    new_frame = np.zeros((500, 500, 3), np.uint8)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    active_letter = keys_set_1[letter_index]

    faces = detector(gray)

    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        landmarks = predictor(gray, face)

        # Eye Blink Detection
        left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
        right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
        blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

        if blinking_ratio >= 3.60:
            cv2.putText(frame, 'BLINK...', (50, 150), font, 4, (0, 0, 255), cv2.LINE_4)
            blinking_frames += 1
            frames -= 1

            if blinking_frames == 1:
                if active_letter == 'Space':
                    active_letter = ' '
                else:
                    active_letter = active_letter
                text += active_letter
        else:
            blinking_frames = 0

    # Letters
    if frames == 10:
        letter_index += 1
        frames = 0

    if letter_index == 28:
        letter_index = 0

    for i in range(28):
        if i == letter_index:
            light = True
        else:
            light = False
        letter(i, keys_set_1[i], light)

    cv2.putText(board, text, (5, 30), font, 2, 0, 3)

    cv2.imshow('frame', frame)
    # cv2.imshow('New Frame', new_frame)
    cv2.imshow('Virtual Keyboard', keyboard)
    cv2.imshow('Board', board)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
