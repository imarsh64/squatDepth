import cv2


def video_resize(cap):
    success, image = cap.read()
    height, width, layers = image.shape
    new_h = int(height / 2.5)
    new_w = int(width / 2.5)
    count = 0

    out = cv2.VideoWriter('resize.mp4', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                          20, (new_w, new_h))

    while success:
        resize = cv2.resize(image, (new_w, new_h))
        out.write(resize)

        success, image = cap.read()
        count += 1

    cap.release()
    out.release()

    return new_w, new_h


def get_positions(results, w, h):
    lm_list = []
    for id, lm in enumerate(results.pose_landmarks.landmark):
        lm_list.append([id, int(lm.x * w), int(lm.y * h), lm.visibility])
    return lm_list


def determine_side(lm_list):
    if lm_list[26][3] > lm_list[25][3]:
        side = 'Right'
    else:
        side = 'Left'

    return side


def good_lift(frame, good):
    if good:
        for i in range(3):
            cv2.circle(frame, (35 + i * 70, 45), 30, (255, 255, 255), cv2.FILLED)
    else:
        for i in range(3):
            cv2.circle(frame, (35 + i * 70, 45), 30, (0, 0, 255), cv2.FILLED)
