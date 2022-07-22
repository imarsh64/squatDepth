import cv2


# Resize video and output to new video
def video_resize(cap):
    success, image = cap.read()
    height, width, layers = image.shape

    # creates 300 X 400 video
    new_h = int(height * (400 / height))
    new_w = int(width * (300 / width))
    
    count = 0

    out = cv2.VideoWriter('resize.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                          20, (new_w, new_h))

    while success:
        resize = cv2.resize(image, (new_w, new_h))
        out.write(resize)

        success, image = cap.read()
        count += 1

    cap.release()
    out.release()

    return new_w, new_h


# Populate list with all the landmarks
def get_positions(results, w, h):
    lm_list = []
    for id, lm in enumerate(results.pose_landmarks.landmark):
        lm_list.append([id, int(lm.x * w), int(lm.y * h), lm.visibility])
    return lm_list


# Determines whether the camera was set on the right side or left side of body
def determine_side(lm_list):
    if lm_list[26][3] > lm_list[25][3]:
        side = 'Right'
    else:
        side = 'Left'

    return side


# Displays while lights if the lift is good and red if the lift isn't at depth
def good_lift(frame, good):
    if good:
        for i in range(3):
            cv2.circle(frame, (25 + i * 30, 25), 15, (255, 255, 255), cv2.FILLED)
    else:
        for i in range(3):
            cv2.circle(frame, (25 + i * 30, 25), 15, (0, 0, 255), cv2.FILLED)


# Draw circles on hip, knee, and ankle and then connect with lines
def draw_skeleton(frame, hip, knee, ankle):
    cv2.line(frame, (hip[1], hip[2]), (knee[1], knee[2]), (0, 255, 0), 2)
    cv2.line(frame, (knee[1], knee[2]), (ankle[1], ankle[2]), (0, 255, 0), 2)

    cv2.circle(frame, (hip[1], hip[2]), 5, (0, 0, 255), cv2.FILLED)
    cv2.circle(frame, (knee[1], knee[2]), 5, (0, 0, 255), cv2.FILLED)
    cv2.circle(frame, (ankle[1], ankle[2]), 5, (0, 0, 255), cv2.FILLED)
