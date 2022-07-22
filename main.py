import cv2
import mediapipe as mp
import utils

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

# Open video and checks if it opens correctly
cap = cv2.VideoCapture('squat2.mp4')
if not cap.isOpened():
    print('Error opening video')

# Initial width and height
width = cap.get(3)
height = cap.get(4)

# Initialize variable for good lift
good = False

# Resizes the video if it's too big
if width > 300 or height > 400:
    width, height = utils.video_resize(cap)
    cap = cv2.VideoCapture('resize.avi')

# Creates output video
out = cv2.VideoWriter('result.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 20, (width, height))

# Plays Video
success = True
while cap.isOpened() and success:
    success, frame = cap.read()
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    lm_list = utils.get_positions(results, width, height)

    # Determines what side the video is shot from and assigns the proper knee and hip
    side = utils.determine_side(lm_list)
    if side == 'Right':
        hip = lm_list[24]
        knee = lm_list[26]
        ankle = lm_list[28]
    elif side == 'Left':
        hip = lm_list[23]
        knee = lm_list[25]
        ankle = lm_list[27]

    if results.pose_landmarks:
        # Checks for depth
        if hip[2] >= knee[2]:
            good = True

        # Changes indicator from red to white if good lift
        utils.good_lift(frame, good)

        # Draw skeleton for the legs
        utils.draw_skeleton(frame, hip, knee, ankle)

        # Writes frame to output video
        out.write(frame)

    cv2.imshow("Frame", frame)
    cv2.waitKey(1)
