import numpy as np
import cv2
# import video

help_message = '''
USAGE: project.py [<video_source>]
(default video_source: laptop camera)

Keys:
 1 - toggle optical flow visualization
 2 - toggle hand contours visualization
 3 - toggle HSV flow visualization

Press 'ESC' to quit.
'''

def draw_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1)
    # y = np.unique(np.nonzero(flow)[:2], axis=1)[0][step/2:h:step]
    # x = np.unique(np.nonzero(flow)[:2], axis=1)[1][step/2:w:step]
    fx, fy = flow[y,x].T
    i = np.unique(np.hstack([np.where(np.abs(fx)>4), np.where(np.abs(fy)>4)]))
    # print max(fx), min(fx)
    # print max(fy), min(fy)
    # lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.vstack([x[i], y[i], x[i]+fx[i], y[i]+fy[i]]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.polylines(vis, lines, 0, (0,255,0))
    for (x1, y1), (x2, y2) in lines:
        cv2.circle(vis, (x1, y1), 1, (0,255,0), -1)
    return vis

def draw_hsv(flow):
    h, w = flow.shape[:2]
    fx, fy = flow[:,:,0], flow[:,:,1]
    ang = np.arctan2(fy, fx) + np.pi
    v = np.sqrt(fx*fx+fy*fy)
    hsv = np.zeros((h, w, 3), np.uint8)
    hsv[...,0] = ang*(180/np.pi/2)
    hsv[...,1] = 255
    hsv[...,2] = np.minimum(v*4, 255)
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return bgr

def draw_handContours(img):
    drawing = np.zeros(img.shape, np.uint8)
    center = (0,0)

    img_ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    # cv2.imshow("img_ycrcb", img_ycrcb)
    img_mask = cv2.inRange(img_ycrcb, skin_l, skin_h)
    img_mask_closing = cv2.morphologyEx(img_mask, cv2.MORPH_CLOSE, kernel)
    # img_mask_opening = cv2.morphologyEx(img_mask, cv2.MORPH_OPEN, kernel)
    img_res = img_mask_closing
    # cv2.imshow('roi_res', img_res)

    contours, hierarchy = cv2.findContours(img_res, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # print len(contours)
    if len(contours):
        # print "contours"
        ci = 0
        max_area = 0

        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            if(area > max_area):
                max_area = area
                ci = i

        cnt = contours[ci]
        # hull = cv2.convexHull(cnt)

        cv2.drawContours(drawing,  [cnt], 0, (255,255,255), 2)
        # cv2.drawContours(drawing, [hull], 0, (0,0,255),     2)

        moments = cv2.moments(cnt)
        if moments['m00']!= 0:
            cx = int(moments['m10']/moments['m00']) # cx = M10/M00
            cy = int(moments['m01']/moments['m00']) # cy = M01/M00
            center = (cx,cy)
            cv2.circle(drawing, center, 5, (0,0,255), 2)

        hull = cv2.convexHull(cnt, returnPoints=False)
        try:
            defects = cv2.convexityDefects(cnt, hull)
            mind = 0
            maxd = 0
            i = 0
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i,0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                dist = cv2.pointPolygonTest(cnt, center, True)
                cv2.line(drawing, start, end, (0,255,0), 2)
                cv2.circle(drawing, far, 5, (255,0,0), -1)
                # print(i)
        except:
            pass

    return center, drawing

def draw_ball(flow, center):
    global posBall
    canh, canw = flow.shape[:2]
    canvas = np.zeros((canh, canw, 3), np.uint8)
    radius = 20
    flow_cent = flow[center[1], center[0]].T
    # print flow_cent
    posBall += 2*np.round(flow_cent).astype(int)
    posBall[0] %= canw
    posBall[1] %= canh
    cv2.circle(canvas, tuple(posBall), radius, (0,255,255), -1)

    return canvas

if __name__ == '__main__':
    import sys
    print help_message
    try: fn = sys.argv[1]
    except: fn = 0

    show_flow = False
    show_handContours = False
    show_hsv = False

    cap = cv2.VideoCapture(fn)
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1, dst=None)

    frh, frw = frame.shape[:2]
    roi_lu = (int(0.5*frw), 0)
    roi_rd = (frw, int(0.7*frh))
    roi_prev = frame[:roi_rd[1], roi_lu[0]:]
    prevgray = cv2.cvtColor(roi_prev, cv2.COLOR_BGR2GRAY)

    # Asian skin color range (YCrCb): Cr(140~175), Cb(77~123)
    skin_l = (0,   140,  77)
    skin_h = (255, 175, 123)

    ksize = 9
    kernel = np.ones((ksize,ksize), np.uint8)

    posBall = [roi_prev.shape[1]/2, roi_prev.shape[0]/2]

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1, dst=None)

        cv2.rectangle(frame, roi_lu, roi_rd, (170,170,0), 2)
        cv2.imshow('capture', frame)

        roi = frame[:roi_rd[1], roi_lu[0]:]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prevgray, gray, 0.5, 3, 15, 3, 5, 1.2, 0)
        prevgray = gray

        center, handContours = draw_handContours(roi)

        cv2.imshow('canvas', draw_ball(flow, center))

        if show_flow:
            cv2.imshow('flow', draw_flow(gray, flow))
        else:
            cv2.destroyWindow('flow')
            # try: cv2.destroyWindow('flow HSV')
            # except: pass
        if show_handContours:
            cv2.imshow('hand contours', handContours)
        else:
            cv2.destroyWindow('hand contours')
        if show_hsv:
            cv2.imshow('flow HSV', draw_hsv(flow))
        else:
            cv2.destroyWindow('flow HSV')
            # try: cv2.destroyWindow('flow HSV')
            # except: pass

        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            break
        if ch == ord('1'):
            show_flow = not show_flow
            print 'Optical flow visualization is', ['off', 'on'][show_flow]
        if ch == ord('2'):
            show_handContours = not show_handContours
            print 'Hand contours visualization is', ['off', 'on'][show_handContours]
        if ch == ord('3'):
            show_hsv = not show_hsv
            print 'HSV flow visualization is', ['off', 'on'][show_hsv]


    cap.release()
    cv2.destroyAllWindows()