#import Libary
import cv2 # read image
import mediapipe as mp # find hand
import pyautogui # get width and hight windonw
import mouse # control mouse

# funtion find hands in image
def find(img):
    results = hands.process(img)
    return results

# funtion find position finger in position hand
def find_x_y_finger(results, W, H):
    finger_x, finger_y = results.x * W, results.y * H
    return finger_x, finger_y

# main funtion
if __name__ == '__main__':
    # pull image by camara
    cap = cv2.VideoCapture(1)

    # get wigth and hight
    W_H = pyautogui.size()

    # set tools find hand 
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    # Loop read images
    while True:
        # read image
        success, img = cap.read()
        # filp img
        img = img[:, ::-1]
        # resize image
        img = cv2.resize(img, W_H)
        # copy image
        img_copy = img.copy()

        # get position hand by image color RGB
        results = find(img[:, :, ::-1])

        # if find position hand
        if results.multi_hand_landmarks:

            # find position midle_finger
            finger_x_one, finger_y_one = find_x_y_finger(results.multi_hand_landmarks[0].landmark[12], W_H[0], W_H[1])
            # find position root pong_finger
            finger_x_two, finger_y_two = find_x_y_finger(results.multi_hand_landmarks[0].landmark[2], W_H[0], W_H[1])

            # drow circle position midle_finger
            cv2.circle(img_copy, (int(finger_x_one), int(finger_y_one)), 50, (255, 0, 0), -1)
            # drow circle position root pong_finger
            cv2.circle(img_copy, (int(finger_x_two), int(finger_y_two)), 50, (255, 0, 0), -1)
            # drow circle position betaween root pong_finger and midle_finger
            cv2.circle(img_copy, (int(finger_x_two+((finger_x_one-finger_x_two)/2)), int(finger_y_one+((finger_y_two-finger_y_one)/2))), 20, (0, 0, 255), -1)


            # cal X and Y short and long
            X = finger_x_one-finger_x_two if finger_x_one-finger_x_two > 0 else finger_x_two-finger_x_one
            Y = finger_y_one-finger_y_two if finger_y_one-finger_y_two > 0 else finger_y_two-finger_y_one

            # object hand
            if X < 170 and Y < 170:
                mouse.press()
                mouse.move(finger_x_one+((finger_x_two-finger_x_one)/2)+10, finger_y_one+((finger_y_two-finger_y_one)/2)+25)
            # beer hand
            else:
                mouse.release()
                mouse.move(finger_x_one+((finger_x_two-finger_x_one)/2)+10, finger_y_one+((finger_y_two-finger_y_one)/2)+25)

        # resize image
        img_copy = cv2.resize(img_copy, (640, 480))
        cv2.imshow('img_copy', img_copy)

        # you can destroyAllWindows by button 'q' down
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
