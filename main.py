import cv2 as cv
import numpy as np
import lanes


video = cv.VideoCapture("road.mp4")

if not video.isOpened():
    print("Could not open video")

cv.waitKey(1)

while video.isOpened():
    _, frame = video.read()


    cv.namedWindow("video", cv.WINDOW_NORMAL)
    cv.resizeWindow("video", 1300, 800)
    copy_img = np.copy(frame)

    try:
        frame = lanes.canny(frame)
        frame = lanes.mask(frame)
        detected_lines = cv.HoughLinesP(frame, 1, np.pi / 180, 50, np.array([()]), minLineLength=30, maxLineGap=150)
        average_lanes = lanes.average_slope_intercept(frame, detected_lines)
        line_image = lanes.display_lines(copy_img, average_lanes)
        filled = lanes.fill_lane(copy_img, average_lanes)
        combo = cv.addWeighted(filled, 0.8, line_image, 0.5, 1)

        cv.imshow("video", combo)
    except:
        pass



    if cv.waitKey(1) & 0xFF == ord('q'):
        video.release()
        cv.destroyAllWindows()


