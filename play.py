import cv2
import sys
import time
import os 
import subprocess
import random
import json
import random

video_class = json.load(open('video_type.json'))


def PlayAndLoad(class_type,video_number,play_comment = False):
    if class_type == 'stressed':
        p = subprocess.Popen("open question.mp4", shell=True)
        time.sleep(16)
    if class_type == 'happy' and play_comment:
        p = subprocess.Popen("open comment.mp4", shell=True)
        time.sleep(7)
    p = subprocess.Popen("open head.mp4", shell=True) 
    time.sleep(5)
    print_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    cap.set(1, 10.0)
    #此处fourcc的在MAC上有效，如果视频保存为空，那么可以改一下这个参数试试, 也可以是-1
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    # 第三个参数则是镜头快慢的，10为正常，小于10为慢镜头    
    item = video_class[class_type][int(video_number)]
    video_name = item[0]
    video_time = item[1]
    out = cv2.VideoWriter('./video/' + class_type +'/output_'+class_type+print_time+'.avi', fourcc, 30, (640, 480))
    p1 = subprocess.Popen("open "+video_name, shell=True) 
    time_start=time.time()
    print(class_type + ' start')
    while True:
        ret,frame = cap.read()
        if ret == True and time.time()-time_start<video_time:
        # if ret == True and time.time()-time_start<10:
            frame = cv2.flip(frame, 1)
            a = out.write(frame)
            # cv2.imshow("frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            pid = p1.pid
            print(pid)
            os.system("kill -9 " + str(pid))
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(class_type + ' end')

import os,getopt,argparse

parser = argparse.ArgumentParser(description = 'File Path')
parser.add_argument("-ha", '--happy', type=str, dest="happy", help="happy number")
parser.add_argument("-ne", "--neutral", type=str, dest="neutral", help="neutral number")
parser.add_argument('-st', "--stressed", type=str, dest="stressed", help='stressed number')
args = parser.parse_args()

need_comment = args.happy and args.neutral and args.stressed
if args.happy:
    PlayAndLoad('happy',args.happy,need_comment)
if args.neutral:
    PlayAndLoad('neutral',args.neutral)
if args.stressed:
    PlayAndLoad('stressed',args.stressed)
