#!/bin/env python
#coding=utf-8
# import zmq
import time
import cv2
import platform
import base64
import requests
import json

system_name = platform.system()
print("SystemName:",system_name)
camera_frame = 150
camera_fps_base = 0.2
cameras = {}

def send_content(content,id_num):
    url = "http://127.0.0.1:8088/api/xc/send_img"
    data = "123"
    params = {
        "num":id_num,
        "content": content,
    }
    d = json.dumps(params)
    r = requests.post(url, data=d)

def send_content_web(content,id_num):
    url = "http://www.hotpoor.org/api/comment/submit_data_free"
    data = "123"
    params = {
        "user_id": "2dd2c53e7c654c66b398e574848d4c34",
        "aim_id": "2dd2c53e7c654c66b398e574848d4c34",
        "app":"hotpoor",
        "content": u"HWEBIMGBASE64//%d_@@_data:image/jpeg;base64,%s"%(id_num,content),
    }
    d = params
    d = json.dumps(params)
    r = requests.post(url, data=d)


def test():
    global cameras,cameras_num
    for i in range(0,10):
        if system_name in ["Darwin"]:
            cap = cv2.VideoCapture(i)
        elif system_name in ["Windows"]:
            cap = cv2.VideoCapture(i,cv2.CAP_DSHOW)
        else:
            # ["Linux"]
            cap = cv2.VideoCapture(i)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,camera_frame)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT,camera_frame)
        test, frame = cap.read()
        print("i:",str(i),"result:",str(test))
        bstime = time.time()
        if test:
            cameras["usb%s"%i]=[cap,i,bstime]
        # cap.release()
def test_list():
    global cameras,cameras_num
    for k,v in cameras.items():
        [cap,i,st] = v
        start = time.time()
        test, frame = cap.read()
        start = time.time()
        frame = cv2.resize(frame, (camera_frame, camera_frame))
        # grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        grayImage = frame
        img_BigSize = cv2.resize(grayImage, (300, 300))
        img_param = [int(cv2.IMWRITE_JPEG_QUALITY), 15]
        encoded, buffer = cv2.imencode('.jpg', grayImage,img_param)
        img_b64 = base64.b64encode(buffer).decode('utf-8')
        # cv2.imshow("CV%s"%str(i), frame)
        
        end = time.time()
        fps_under = end - start
        if fps_under == 0:
            fps = 1
        else:
            fps = 1 / (end - start)
        print("video:",i,":",len(img_b64),"FPS:{:.0f}".format(fps),"%s %s"%(start,end))
        send_content_web(img_b64,i)
        # if start - st >camera_fps_base:
        #     st = start
        #     cameras[k][2]=st
        # else:
        #     continue
test()
while 1:
    test_list()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
for cap,i in cameras:
    cap.release()
cv2.destroyAllWindows() 