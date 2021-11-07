import threading
from typing import Tuple
from up_controller import UpController
import time
import cv2
import apriltag
import sys
import numpy as np
import math

frame = cv2.VideoCapture(0)
at_detector = apriltag.Detector(apriltag.DetectorOptions(families='tag36h11'))  # 创建一个apriltag检测器


class MatchDemo:

    

    FD = 150
    RD = 150
    BD = 150
    LD = 180

    # 倾斜计时
    na = 0
    # 推箱子计时
    nb = 0
    # 旋转计时
    nc = 0
    # 前搁浅计时
    nd = 0
    # 后搁浅计时
    ne = 8
    # 倾斜
    qx = 0

    def __init__(self):
        self.version = "1.0"
        self.servo_speed = 1023
        self.controller = UpController()
        self.controller.lcd_display("MatchDemo")
        # 设置
        self.controller.set_chassis_mode(0)
        motor_ids = [1, 2] 
        servo_ids = [5, 6, 7, 8]
        self.controller.set_cds_mode(motor_ids, 1)
        self.controller.set_cds_mode(servo_ids, 0)
        
        self.at_detector = apriltag.Detector(apriltag.DetectorOptions(families='tag36h11 tag25h9'))
        self.apriltag_width = 0
        self.tag_id = -1
        apriltag_detect = threading.Thread(target = self.apriltag_detect_thread)
        apriltag_detect.setDaemon(True)
        # apriltag_detect.start()
    
    def save_img(img,tag_id):
        i=0
        cv2.imwrite("./imgs" + tag_id + "_" + i + ".jpg",img)
        i= i + 1
        

    def apriltag_detect_thread(self,img):
        img = img[100:]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        tags = at_detector.detect(gray)  # 进行apriltag检测，得到检测到的apriltag的列表
        # print("%d apriltags have been detected."%len(tags))
        # if len(tags) == 0:
            # ser.write("4".encode("gb18030"))
        key_longest_side = [-1, -1, -1]

        for tag in tags:
            x0, y0 = tuple(tag.corners[0].astype(int))
            x1, y1 = tuple(tag.corners[1].astype(int))
            x2, y2 = tuple(tag.corners[2].astype(int))
            x3, y3 = tuple(tag.corners[3].astype(int))

            d_up = math.sqrt(math.pow((x1 - x0), 2) + math.pow((y1 - y0), 2))
            d_down = math.sqrt(math.pow((x3 - x2), 2) + math.pow((y3 - y2), 2))
            d_left = math.sqrt(math.pow((x3 - x0), 2) + math.pow((y3 - y0), 2))
            d_right = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
            if (tag.tag_id) < 3 :
                if d_up >= d_down and d_up >= d_left and d_up >= d_right :  #get_longest_side
                    key_longest_side[tag.tag_id] = d_up
                elif d_down >= d_up and d_down >= d_left and d_down >= d_right :
                    key_longest_side[tag.tag_id] = d_down
                elif d_left >= d_up and d_left >= d_down and d_left >= d_right :
                    key_longest_side[tag.tag_id] = d_left
                elif d_right >= d_up and d_right >= d_down and d_right >= d_left :
                    key_longest_side[tag.tag_id] = d_right
            else :
                print("The id not in list!")

        key_index = -1 #save_longest_side_side
        if key_longest_side[0] >= key_longest_side[1] and key_longest_side[0] >= key_longest_side[2]:
            key_index = 0
        elif key_longest_side[1] >= key_longest_side[0] and key_longest_side[1] >= key_longest_side[2]:
            key_index = 1
        elif key_longest_side[2] >= key_longest_side[0] and key_longest_side[2] >= key_longest_side[1]:
            key_index = 2
        print(key_longest_side)
        for tag in tags:
            if tag.tag_id == key_index:
                print(tag.tag_id)
                return tag.tag_id
        # print("detect start")
        # cap = cv2.VideoCapture(2)

        # w = 640
        # h = 480
        # weight = 320
        # cap.set(3,w)
        # cap.set(4,h)

        # cup_w = (int)((w - weight) / 2)
        # cup_h = (int)((h - weight) / 2) + 50

        # while True:
        #     ret, frame = cap.read()
        #     #frame = frame[cup_h:cup_h + weight,cup_w:cup_w + weight]
        #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #     tags = self.at_detector.detect(gray)
        #     for tag in tags:
        #         self.tag_id = tag.tag_id
        #         print("tag_id = {}".format(tag.tag_id))
        #         cv2.circle(frame, tuple(tag.corners[0].astype(int)), 4, (255, 0, 0), 2) # left-top
        #         cv2.circle(frame, tuple(tag.corners[1].astype(int)), 4, (255, 0, 0), 2) # right-top
        #         cv2.circle(frame, tuple(tag.corners[2].astype(int)), 4, (255, 0, 0), 2) # right-bottom
        #         cv2.circle(frame, tuple(tag.corners[3].astype(int)), 4, (255, 0, 0), 2) # left-bottom
        #     cv2.imshow("img", frame)
        #     if cv2.waitKey(100) & 0xff == ord('q'):
        #        break
        # cap.release()
        # cv2.destroyAllWindows()

    # 默认上台动作
    def default_platform(self):
        self.controller.up.CDS_SetAngle(5, 630, self.servo_speed)
        self.controller.up.CDS_SetAngle(6, 600, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 330, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 340, self.servo_speed)

    # 放下前爪
    def pack_up_ahead(self):
        self.controller.up.CDS_SetAngle(5, 300, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 650, self.servo_speed)
        time.sleep(0.01)
        self.controller.up.CDS_SetAngle(5, 300, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 650, self.servo_speed)

    # 放下后爪
    def pack_up_behind(self):
        self.controller.up.CDS_SetAngle(6, 280, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 650, self.servo_speed)
        time.sleep(0.01)
        self.controller.up.CDS_SetAngle(6, 280, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 650, self.servo_speed)


    # 上台后爪子的状态
    def shovel_state(self):
        self.controller.up.CDS_SetAngle(5, 300, self.servo_speed)
        self.controller.up.CDS_SetAngle(6, 300, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 650, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 700, self.servo_speed)

    # 前上台动作
    def go_up_ahead_platform(self):
        self.controller.move_cmd(0, 0)
        time.sleep(0.1)
        # 爪子抬起
        self.default_platform()
        time.sleep(0.4)
        self.controller.move_cmd(800, 800)
        time.sleep(1)
        # 支前爪
        self.controller.move_cmd(0, 0)
        self.controller.up.CDS_SetAngle(5, 300, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 680, self.servo_speed)
        # self.pack_up_ahead()
        time.sleep(0.5)
        # 收起前爪
        self.controller.move_cmd(1023,1023)
        time.sleep(0.5)
        self.controller.move_cmd(0,0)
        time.sleep(0.3)
        self.controller.move_cmd(1023,1023)
        time.sleep(0.3)
        self.controller.up.CDS_SetAngle(5, 630, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 300, self.servo_speed)
        # 支后爪
        #time.sleep(0.5)
        # self.pack_up_behind()
        self.controller.up.CDS_SetAngle(6, 270, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 680, self.servo_speed)
        time.sleep(1)
        # 默认上台
        self.controller.up.CDS_SetAngle(6, 600, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 340, self.servo_speed)
        # self.default_platform()
        self.controller.move_cmd(0, 0)
        #time.sleep(0.5)     
        # time.sleep(0.5)

    # 后上台
    def go_up_behind_platform(self):
        self.controller.move_cmd(0, 0)
        time.sleep(0.1)
        # 爪子抬起
        self.default_platform()
        time.sleep(0.4)
        self.controller.move_cmd(-800, -800)
        time.sleep(1)
        # 支前爪
        self.controller.move_cmd(0,0)
        # self.pack_up_behind()
        self.controller.up.CDS_SetAngle(6, 270, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 680, self.servo_speed)
        time.sleep(0.5)
        # 收起前爪
        self.controller.move_cmd(-1023,-1023)
        time.sleep(0.5)
        self.controller.move_cmd(0,0)
        time.sleep(0.3)
        self.controller.move_cmd(-1023,-1023)
        time.sleep(0.3)
        self.controller.up.CDS_SetAngle(6, 600, self.servo_speed)
        self.controller.up.CDS_SetAngle(8, 340, self.servo_speed)
        # 支后爪
        #time.sleep(0.5)
        # self.pack_up_ahead()
        self.controller.up.CDS_SetAngle(5, 300, self.servo_speed)
        self.controller.up.CDS_SetAngle(7, 680, self.servo_speed)
        time.sleep(1)
        # 默认上台
        self.controller.up.CDS_SetAngle(5,650,self.servo_speed)
        self.controller.up.CDS_SetAngle(7,300,self.servo_speed)
        self.default_platform()
        #time.sleep(0.5)
        self.controller.move_cmd(0, 0)
        #time.sleep(0.5)

    # 检测是否在台上-返回状态
    def paltform_detect(self):
        angle_sensor = self.controller.adc_data[0]
        ahead_ad = 1 if self.controller.adc_data[5] < 1000 else 0
        right_ad = 1 if self.controller.adc_data[6] < 1000 else 0
        behind_ad = 1 if self.controller.adc_data[7] < 1000 else 0
        left_ad = 1 if self.controller.adc_data[8] < 1000 else 0
        left_ahead_io = 1 if self.controller.io_data[0] == 0 else 0
        right_ahead_io = 1 if self.controller.io_data[1] == 0 else 0
        right_behind_io = 1 if self.controller.io_data[2] == 0 else 0
        left_behind_io = 1 if self.controller.io_data[3] == 0 else 0
        sum_down = ahead_ad + right_ad + behind_ad + left_ad
        sum_up = left_ahead_io + left_behind_io + right_ahead_io + right_behind_io
        # if angle_sensor > 1500 and angle_sensor < 2100:
        if sum_down >= 1 and sum_up <= 2:
            # 在台下
            return 0
        elif sum_down == 0 and sum_up == 0:
            return 5
        else:
            # 在台上
            return 1
        # elif angle_sensor <= 1500:
        #     # 卡在擂台左侧在地面右侧在擂台
        #     return 3
        # else:
        #     # 卡在擂台右侧在地面左侧在擂台
        #     return 4

    def fence_detect(self):
        # 底部前方红外光电
        ad1 = self.controller.adc_data[5]
        # 底部右侧红外光电
        ad2 = self.controller.adc_data[6]
        # 底部后方红外光电
        ad3 = self.controller.adc_data[7]
        # 底部左侧红外光电
        ad4 = self.controller.adc_data[8]

        # 前红外测距传感器
        ad5 = self.controller.adc_data[1]
        # 右红外测距传感器
        ad6 = self.controller.adc_data[2]
        # 后红外测距传感器
        ad7 = self.controller.adc_data[3]
        # 左红外测距传感器
        ad8 = self.controller.adc_data[4]


        # ----------------------对擂台，一个测距检测到--------------------
        if ad3 < 1000 and ad2 > 1000 and ad4 > 1000 and ad5 > self.FD and ad6 < self.RD and ad7 < self.BD and ad8 < self.LD:
            # 在台下，后方对擂台
            return 1
        if ad4 < 1000 and ad1 > 1000 and ad3 > 1000 and ad5 < self.FD and ad6 > self.RD and ad7 < self.BD and ad8 < self.LD:
            # 在台下，左侧对擂台
            return 2
        if ad1 < 1000 and ad2 > 1000 and ad4 > 1000 and ad5 < self.FD and ad6 < self.RD and ad7 > self.BD and ad8 < self.LD:
            # 在台下，前方对擂台
            return 3
        if ad2 < 1000 and ad1 > 1000 and ad3 > 1000 and ad5 < self.FD and ad6 < self.RD and ad7 < self.BD and ad8 > self.LD:
            # 在台下，右侧对擂台
            return 4

        # ------------------------对围栏，两个相邻测距检测到-------------
        if ad2 > 1000 and ad3 > 1000 and ad5 > self.FD and ad6 < self.RD and ad7 < self.BD and ad8 > self.LD:
            # 在台下，前左检测到围栏
            return 5

        if ad3 > 1000 and ad4 > 1000 and ad5 > self.FD and ad6 > self.RD and ad7 < self.BD and ad8 < self.LD:
            # 在台下，前右检测到围栏
            return 6
        if ad1 > 1000 and ad4 > 1000 and ad5 < self.FD and ad6 > self.RD and ad7 > self.BD and ad8 < self.LD:
            # 在台下，后右检测到围栏
            return 7
        if ad1 > 1000 and ad2 > 1000 and ad5 < self.FD and ad6 < self.RD and ad7 > self.BD and ad8 > self.LD:
            # 在台下，后左检测到围栏
            return 8

        # --------------------------台上有敌人，两个相对测距检测到-----------
        if ad5 > self.FD and ad6 < self.RD and ad7 > self.BD and ad8 < self.LD:
            # 在台下，前方或后方有台上敌人
            return 9
        if ad5 < self.FD and ad6 > self.RD and ad7 < self.BD and ad8 > self.LD:
            # 在台下，左侧或右侧由台上敌人
            return 10

        # -------------------------三侧有障碍，三个测距检测到---------------
        if ad5 > self.FD and ad6 > self.RD and ad7 < self.BD and ad8 > self.LD:
            # 在台下，前方、左侧和右侧检测到围栏
            return 11
        if ad5 > self.FD and ad6 > self.RD and ad7 > self.BD and ad8 < self.LD:
            # 在台下，前方、右侧和后方检测到围栏
            return 12
        if ad5 > self.FD and ad6 < self.RD and ad7 > self.BD and ad8 > self.LD:
            # 在台下，前方、左侧和后方检测到围栏
            return 13
        if ad5 < self.FD and ad6 > self.RD and ad7 > self.BD and ad8 > self.LD:
            # 在台下，右侧、左侧和后方检测到围栏
            return 14

        # -----------------------斜对擂台，两个红外光电检测到----------------
        if ad1 < 1000 and ad2 < 1000 and ad5 < self.FD and ad6 < self.RD:
            # 在台下，前方和右侧对擂台其他传感器没检测到
            return 15
        if ad1 < 1000 and ad4 < 1000 and ad5 < self.FD and ad8 < self.LD:
            # 在台下，在台下，前方和左侧对擂台其他传感器没检测到
            return 16
        if ad2 < 1000 and ad3 < 1000 and ad6 < self.FD and ad7 < self.RD:
            # 在台下，后方和右侧对擂台其他传感器没检测到
            return 17
        if ad3 < 1000 and ad4 < 1000 and ad7 < self.FD and ad8 < self.LD:
            # 在台下，后方和左侧对擂台其他传感器没检测到
            return 18
        if ad1 > 1000 and ad2 > 1000 and ad3 < 1000 and ad4 > 1000:
            return 19
        if ad1 < 1000 and ad2 > 1000 and ad3 > 1000 and ad4 > 1000:
            return 20
        # 底部前方红外光电
        # ad1 = self.controller.adc_data[5]
        # 底部右侧红外光电
        # ad2 = self.controller.adc_data[6]
        # 底部后方红外光电
        # ad3 = self.controller.adc_data[7]
        # 底部左侧红外光电
        # ad4 = self.controller.adc_data[8]
        else:
            print("else")
            return 101


    def edge_detect(self):
        # 左前红外光电传感器
        io_0 = self.controller.io_data[0]
        # 右前红外光电传感器
        io_1 = self.controller.io_data[1]
        # 右后红外光电传感器
        io_2 = self.controller.io_data[2]
        # 左后红外光电传感器
        io_3 = self.controller.io_data[3]
        # 获取前方测距值
        ad5 = self.controller.adc_data[1]
        # 获取后方测距值
        ad7 = self.controller.adc_data[3]

        if io_0 == 0 and io_1 == 0 and io_2 == 0 and io_3 == 0:
            # 没有检测到边缘
            return 0
        elif io_0 == 1 and io_1 == 0 and io_2 == 0 and io_3 == 0:
            # 左前检测到边缘
            return 1
        elif io_0 == 0 and io_1 == 1 and io_2 == 0 and io_3 == 0:
            # 右前检测到边缘
            return 2
        elif io_0 == 0 and io_1 == 0 and io_2 == 1 and io_3 == 0:
            # 右后检测到边缘
            return 3
        elif io_0 == 0 and io_1 == 0 and io_2 == 0 and io_3 == 1:
            # 左后检测到边缘
            return 4
        elif io_0 == 1 and io_1 == 1 and io_2 == 0 and io_3 == 0:
            # 前方两个检测到边缘
            return 5
        elif io_0 == 0 and io_1 == 0 and io_2 == 1 and io_3 == 1:
            # 后方两个检测到边缘
            return 6
        elif io_0 == 1 and io_1 == 0 and io_2 == 0 and io_3 == 1:
            # 左侧两个检测到边缘
            return 7
        elif io_0 == 0 and io_1 == 1 and io_2 == 1 and io_3 == 0:
            # 右侧两个检测到边缘
            return 8
        elif io_0 == 1 and io_1 == 1 and io_2 == 1 and io_3 == 1 and ad5 > 480:
            # 搁浅放在擂台下
            return 9
        elif io_0 == 1 and io_1 == 1 and io_2 == 1 and io_3 == 1 and ad7 > 480:
            # 搁浅放在擂台上
            return 10
        else:
            return 102

    # 敌人检测
    def enemy_detect(self):
        # 底部前方红外光电
        ad1 = self.controller.adc_data[5]
        # 底部右侧红外光电
        ad2 = self.controller.adc_data[6]
        # 底部后方红外光电
        ad3 = self.controller.adc_data[7]
        # 底部左侧红外光电
        ad4 = self.controller.adc_data[8]
        # 前红外测距传感器
        ad5 = self.controller.adc_data[1]

        #print("ad1 = {} , ad2 = {} , ad3 = {}, ad4 = {} , ad5 = {}".format(ad1,ad2,ad3,ad4,ad5))

        if ad1 > 100 and ad2 > 100 and ad3 > 100 and ad4 > 100:
            # 无敌人
            return 0
        if ad1 < 100 :
            return 1
            # if ad5 > 1000:
            #     # 前方是箱子
            #     return 11
            # else:
            #     # 前方有敌人
            #     if self.tag_id != 2 or self.tag_id == -1:
            #         # 前方是敌人
            #         return 1
            #     else:
            #         return 5
        elif ad3 < 100 :
            # 后方有敌人或棋子
            return 3
        elif (ad1 > 100 and ad2 < 100 and ad3 > 100 and ad4 > 100) or (ad1 > 100 and ad2 < 100 and ad3 > 100 and ad4 < 100):      
            # 右侧有敌人或棋子 or 左右两侧都有障碍
            return 2
        elif ad1 > 100 and ad2 > 100 and ad3 > 100 and ad4 < 100:
            # //左侧有敌人或棋子
            return 4
        else:
            return 103


    def start_match(self):
        self.default_platform()    #收起四个铲子
        time.sleep(1)
        ad4 = self.controller.adc_data[8]
        while(ad4 >= 100):
            ad4 = self.controller.adc_data[8]
        self.go_up_ahead_platform()    #前上台
        # self.go_up_behind_platform()
        self.controller.move_cmd(600,700)
        time.sleep(0.5)
        while 1:
            stage = self.paltform_detect()    #检测是否在台上
            ret,img = frame.read()
            # self.default_platform()
            time.sleep(0.01)
            # 在台下
            if stage == 0:
                print("stage",stage,"在台下")
                self.default_platform()
                fence = self.fence_detect()     #获取底部光电及红外测距传感器参数
                print("fence",fence)
                # 在台下后方对擂台
                if fence == 1:
                    self.controller.move_cmd(600,600)
                    time.sleep(0.3)
                    print("fence",fence,"在台下后方对擂台")
                    self.go_up_behind_platform()    #后上台
                
                # 左侧对擂台
                if fence == 2:
                    print("fence",fence,"在台下左侧对擂台")
                    self.controller.move_cmd(800, -800)
                    time.sleep(0.2)
                    t = time.time()
                    while 1:
                        ad1 = self.controller.adc_data[5]
                        ad4 = self.controller.adc_data[8]
                        ad6 = self.controller.adc_data[2]
                        if ad1 < 1000 and ad6 < 160 and ad4 > 1000 or (time.time() - t) >= 5:     #已调整至面向擂台
                            time.sleep(0.2)
                            self.controller.move_cmd(600, 600)
                            time.sleep(0.3)
                            break
                        else:       #为完成面向擂台调整，持续修正
                            self.controller.move_cmd(-600, 600)
                            time.sleep(0.002)
                
                # 前方对擂台
                if fence == 3:
                    print("fence",fence,"在台下前方对擂台")
                    self.controller.move_cmd(-600,-600)
                    time.sleep(0.2)
                    self.go_up_ahead_platform()
                
                # 右侧对擂台
                if fence == 4:
                    print("fence",fence,"在台下右侧对擂台")
                    self.controller.move_cmd(-800, 800)
                    time.sleep(0.2)
                    t = time.time()
                    while 1:
                        ad1 = self.controller.adc_data[5]
                        ad4 = self.controller.adc_data[8]
                        ad6 = self.controller.adc_data[2]
                        if ad1 < 1000 and ad6 < 160 and ad4 > 1000 or (time.time() - t) >= 5:     #与’左侧对擂台‘调整过程类似
                            time.sleep(0.2)
                            self.controller.move_cmd(600, 600)
                            time.sleep(0.3)
                            break
                        else:
                            self.controller.move_cmd(600, -600)
                            time.sleep(0.02)
                
                # 前左检测到围栏
                if fence == 5:      #距离擂台过近，作后退调整，与下方相同
                    print("fence",fence,"在台下，前左检测到擂台")
                    self.controller.move_cmd(-600, -600)
                    time.sleep(0.4)
                # 前右检测到围栏
                if fence == 6:
                    print("fence",fence,"在台下，前右检测到擂台")
                    self.controller.move_cmd(-600, -600)
                    time.sleep(0.4)
                # 后有检测到围栏
                if fence == 7:      #依然是过近，不过是做前进调整
                    print("fence",fence,"在台下，后右检测到擂台")
                    self.controller.move_cmd(600, 600)
                    time.sleep(0.4)
                # 后左检测到围栏
                if fence == 8:
                    print("fence",fence,"在台下，后左检测到擂台")
                    self.controller.move_cmd(600, 600)
                    time.sleep(0.4)
                
                # 前方或后方有台上敌人
                if fence == 9:      #先自转，在前进，避开敌人，换个位置上台
                    print("fence",fence,"在台下，前方或后方有台上敌人")
                    self.controller.move_cmd(700, -700)
                    time.sleep(0.3)
                    self.controller.move_cmd(600, 600)
                    time.sleep(0.4)
                # 左侧或右侧有台上敌人
                if fence == 10:     #直接前进，换个位置上台
                    print("fence",fence,"在台下，左侧或右侧有台上敌人")
                    self.controller.move_cmd(600, 600)
                    time.sleep(0.4)
                
                # 前方、左侧和右侧检测到围栏
                if fence == 11:         #此处四种情况不知机器人处于什么状态
                    print("fence",fence,"在台下，前方、左侧和右侧检测到围栏")
                    self.controller.move_cmd(-600, -500)
                    time.sleep(0.5)
                    self.controller.move_cmd(-600, 600)
                    time.sleep(0.3)
                # 前右后检测到围栏
                if fence == 12:
                    print("fence",fence,"在台下，前右后检测到围栏")
                    self.controller.move_cmd(500, 800)
                    time.sleep(0.4)
                # 前左后检测到围栏
                if fence == 13:
                    print("fence",fence,"在台下，前左后检测到围栏")
                    self.controller.move_cmd(800, 500)
                    time.sleep(0.4)
                # 右左后检测到围栏
                if fence == 14:
                    print("fence",fence,"在台下，右左后检测到围栏")
                    self.controller.move_cmd(-600, 600)
                    time.sleep(0.2)
                    self.controller.move_cmd(600, 600)
                    time.sleep(0.3)
                
                # 前右检测到擂台
                if fence == 15:     #与‘右侧对擂台’处理过程相同
                    print("fence",fence,"在台下，前右检测到擂台")
                    self.controller.move_cmd(-600, -600)
                    time.sleep(0.5)
                    self.controller.move_cmd(600, 600)
                    time.sleep(0.5)
                    t = time.time()
                    while 1:
                        ad1 = self.controller.adc_data[5]
                        ad4 = self.controller.adc_data[8]
                        ad6 = self.controller.adc_data[2]
                        if ad1 < 1000 and ad6 < 160 and ad4 > 1000:
                            #time.sleep(0.2)
                            self.controller.move_cmd(600, 600)
                            time.sleep(0.3)
                            break
                        else:
                            if (time.time() - t == 2) :
                                break
                            self.controller.move_cmd(1000, 0)
                            time.sleep(0.5)
                #  前左检测到擂台
                if fence == 16:     #与‘左侧对擂台’处理过程相同
                    print("fence",fence,"在台下，前左检测到擂台")
                    self.controller.move_cmd(-600, -600)
                    time.sleep(0.5)
                    self.controller.move_cmd(600, 600)
                    time.sleep(0.5)
                    t = time.time()
                    while 1:
                        ad1 = self.controller.adc_data[5]
                        ad4 = self.controller.adc_data[8]
                        ad6 = self.controller.adc_data[2]
                        if ad1 < 1000 and ad6 < 160 and ad4 > 1000:
                            # time.sleep(0.2)
                            self.controller.move_cmd(600, 600)
                            time.sleep(0.3)
                            break
                        else:
                            if (time.time() - t == 2) :
                                break
                            self.controller.move_cmd(0, 1000)
                            time.sleep(0.5)
                # 在台下，后方和右侧对擂台其他传感器没检测到
                if fence == 17:         #不知处于什么状态，但解决方法与‘右侧对擂台’相似（自转速度不同）
                    print("fence",fence,"在台下，后方和右侧对擂台其他传感器没检测到")
                    self.controller.move_cmd(0, 0)
                    time.sleep(0.2)
                    while 1:
                        ad1 = self.controller.adc_data[5]
                        ad4 = self.controller.adc_data[8]
                        ad6 = self.controller.adc_data[2]
                        if ad1 < 1000 and ad6 < 160 and ad4 > 1000:
                            time.sleep(0.2)
                            self.controller.move_cmd(600, 600)
                            time.sleep(0.3)
                            break
                        else:
                            self.controller.move_cmd(600, -700)
                            time.sleep(0.002)
                # 在台下,后方和左侧对擂台其他传感器没检测到
                if fence == 18:         #同上
                    print("fence",fence,"在台下，后方和左侧对擂台其他传感器没检测到")
                    self.controller.move_cmd(0, 0)
                    time.sleep(0.2)
                    while 1:
                        ad1 = self.controller.adc_data[5]
                        ad4 = self.controller.adc_data[8]
                        ad6 = self.controller.adc_data[2]
                        if ad1 < 1000 and ad6 < 160 and ad4 > 1000:
                            time.sleep(0.2)
                            self.controller.move_cmd(600, 600)
                            time.sleep(0.3)
                            break
                        else:
                            self.controller.move_cmd(-620, 550)
                            time.sleep(0.002)
                if fence == 19:
                    print("后光电检测到障碍")
                    self.controller.move_cmd(800,800)
                    # self.pack_up_behind()
                if fence == 20:
                    print("前光电检测到障碍")
                    self.controller.move_cmd(-800,-800)
                    # self.pack_up_ahead()

            #在擂台上
            if stage == 1:
                print("stage",stage,"在台上")
                self.na = 0
                self.nb = 0
                edge = self.edge_detect()
                if edge == 0:
                    print("edge",edge,"未检测到边缘")
                    self.pack_up_ahead()
                    self.pack_up_behind()
                    enemy = self.enemy_detect()
                    print("enemy",enemy)
                    # 无敌人
                    if enemy == 0:      #无敌人无箱子，缓速前进
                        print("enemy",enemy,"无敌人无箱子")
                        self.controller.move_cmd(600, 600)
                        # time.sleep(0.01)
                    # 前有qizi
                    elif enemy == 1:      #前方敌人，加速前进
                        # frame = cv2.VideoCapture(1)
                        ret,img = frame.read()
                        id = self.apriltag_detect_thread(img)
                        # self.save_img(img,id)
                        # self.controller.move_cmd(0,0)
                        # time.sleep(1)
                        print("id =", id)
                        if (id != 2): #and (self.edge_detect() == 0) : #如果是1，就绕开
                            print("enemy",enemy,"前方有敌人")
                            self.controller.move_cmd(600, 600)
                            self.pack_up_ahead
                            # time.sleep(0.5)
                            # self.default_platform()
                            # time.sleep(1)
                        elif (id == 2 or id == None) :
                            self.controller.move_cmd(-800,-800)
                            time.sleep(0.5)
                            self.controller.move_cmd(800,-800)
                            time.sleep(1)
                            self.controller.move_cmd(600,600)
                            time.sleep(0.5)
                        # self.pack_up_ahead()
                        # time.sleep(0.001)
                    # 右侧有敌人
                    elif enemy == 2:      #右侧有敌人，先退后(此处的退后目的是刹车，因为执行时间只有0.1s)再原地右转
                        print("enemy",enemy,"右侧有敌人")
                        self.controller.move_cmd(0,0)
                        time.sleep(0.3)
                        #print("ad1","                                                     ",ad1)
                        ad1 = self.controller.adc_data[5]
                        t = time.time()
                        while(ad1 > 100):
                            ad1 = self.controller.adc_data[5]
                            #print("ad1","                                                     ",ad1)
                            self.controller.move_cmd(700, -700)
                            # self.default_platform()
                            if time.time() - t >= 3:    #timeout
                                break
                        self.controller.move_cmd(0,0)
                        time.sleep(0.1)
                        #time.sleep(0.5)
                    # 后方有敌人
                    elif enemy == 3:      #直接原地掉头
                        print("enemy",enemy,"后方有敌人")
                        self.controller.move_cmd(0,0)
                        time.sleep(0.3)
                        ad1 = self.controller.adc_data[5]
                        t = time.time()
                        while(ad1 > 100):
                            ad1 = self.controller.adc_data[5]
                            #print("ad1","                                                     ",ad1)
                            self.controller.move_cmd(-800, 800)
                            # self.default_platform()
                            if time.time() - t >= 3:    #timeout
                                break
                        self.controller.move_cmd(0,0)
                        time.sleep(0.1)
                        #time.sleep(1.0)
                    # 左侧有敌人
                    elif enemy == 4:      #先后退，再左转
                        print("enemy",enemy,"左侧有敌人")
                        self.controller.move_cmd(0,0)
                        time.sleep(0.3)
                        #print("ad1","                                                     ",ad1)
                        ad1 = self.controller.adc_data[5]
                        t = time.time()
                        while(ad1 > 100):
                            ad1 = self.controller.adc_data[5]
                            #print("ad1","                                                     ",ad1)
                            self.controller.move_cmd(-700, 700)
                            # self.default_platform()
                            if time.time() - t >= 3:    #timeout
                                break
                        self.controller.move_cmd(0,0)
                        time.sleep(0.1)
                        #time.sleep(0.5)
                    #  己方箱子
                    # if enemy == 5:      #后退，左转，前进
                    #     print("enemy",enemy,"己方箱子")
                    #     self.controller.move_cmd(-600, -600)
                    #     time.sleep(0.2)
                    #     self.controller.move_cmd(-600, 600)
                    #     time.sleep(0.5)
                    #     self.controller.move_cmd(600, 600)
                    #     time.sleep(0.4)
                    # # 前方检测到箱子
                    # if enemy == 11:     #加速前进
                    #     print("enemy",enemy,"前方箱子")
                    #     id = self.apriltag_detect_thread(img)
                    #     print("id =", id)
                    #     if (id != 1):
                    #         self.controller.move_cmd(600, 600)
                    #         time.sleep(0.3)
                    #         self.pack_up_ahead()
                    #         time.sleep(0.5)
                    #     else :
                    #         self.controller.move_cmd(-600,-600)
                    #         time.sleep(0.5)
                    #         self.controller.move_cmd(800,-800)
                    #         time.sleep(1)
                    #         self.controller.move_cmd(600,600)
                    #         time.sleep(1)
                    #     self.pack_up_ahead()
                    #     # time.sleep(0.001)
                        
                # 左前检测到边缘
                elif edge == 1:       #后退，右转
                    print("edge",edge,"左前检测到边缘")
                    self.default_platform()
                    self.controller.move_cmd(-600, -600)
                    time.sleep(1)
                    self.controller.move_cmd(0,0)
                    time.sleep(0.3)
                    self.controller.move_cmd(800, -800)
                    self.pack_up_ahead()
                    self.pack_up_behind()
                    time.sleep(1)
                # 右前检测到边缘
                elif edge == 2:       #后退，左转
                    print("edge",edge,"右前检测到边缘")
                    self.default_platform()
                    self.controller.move_cmd(-600, -600)
                    time.sleep(1)
                    self.controller.move_cmd(0,0)
                    time.sleep(0.3)
                    self.controller.move_cmd(-800, 800)
                    self.pack_up_ahead()
                    self.pack_up_behind()
                    time.sleep(0.5)
                # 右后检测到边缘
                elif edge == 3:       #前进，右转
                    print("edge",edge,"右后检测到边缘")
                    self.controller.move_cmd(600, 600)
                    time.sleep(1)
                    self.controller.move_cmd(0,0)
                    time.sleep(0.3)
                    self.controller.move_cmd(800, -800)
                    self.pack_up_ahead()
                    self.pack_up_behind()
                    time.sleep(0.5)
                # 左后检测到边缘
                elif edge == 4:       #前进，左转
                    print("edge",edge,"左后检测到边缘")
                    self.default_platform()
                    self.controller.move_cmd(600, 600)
                    time.sleep(1)
                    self.controller.move_cmd(0,0)
                    time.sleep(0.3)
                    self.controller.move_cmd(-800, 800)
                    self.pack_up_ahead()
                    self.pack_up_behind()
                    time.sleep(0.5)
                # 前方两个检测到边缘
                elif edge == 5:       #后退，右转
                    print("edge",edge,"前方检测到边缘")
                    self.default_platform()
                    self.controller.move_cmd(-700, -700)
                    time.sleep(1)
                    self.controller.move_cmd(0,0)
                    time.sleep(0.3)
                    self.controller.move_cmd(800, -800)
                    self.pack_up_ahead()
                    self.pack_up_behind()
                    time.sleep(0.5)
                # 后方两个检测到边缘
                elif edge == 6:       #前进
                    print("edge",edge,"后方检测到边缘")
                    self.default_platform()
                    self.controller.move_cmd(700, 700)
                    time.sleep(1)
                # 左侧两个检测到边缘
                elif edge == 7:       #右转，前进
                    print("edge",edge,"左侧检测到边缘")
                    self.default_platform()
                    self.controller.move_cmd(800, -800)
                    time.sleep(0.5)
                    self.controller.move_cmd(600,600)
                    time.sleep(0.3)
                # 右侧两个检测到边缘
                elif edge == 8:
                    self.controller.move_cmd(-800, 800)
                    self.default_platform()
                    time.sleep(0.5)
                    self.controller.move_cmd(600, 600)
                    time.sleep(0.3)
                # 搁浅前在底下
                elif edge == 9:
                    self.nd += 1
                    if self.nd > 20:
                        self.nd = 0
                        self.controller.move_cmd(0, 0)
                        time.sleep(0.01)
                        self.controller.move_cmd(-800, -800)
                        time.sleep(0.2)
                        self.go_up_ahead_platform()
                        self.controller.move_cmd(-800, -800)
                        time.sleep(0.8)
                        self.default_platform()
                        self.controller.move_cmd(-800, -800)
                        time.sleep(0.5)
                        self.controller.move_cmd(800, -800)
                        time.sleep(0.3)
                        self.controller.move_cmd(0, 0)
                        time.sleep(0.1)
                    else:
                        time.sleep(0.02)
                elif edge == 10:
                    self.ne += 1
                    if self.ne > 20:
                        self.ne = 0
                        self.controller.move_cmd(0, 0)
                        time.sleep(0.01)
                        self.controller.move_cmd(800, 800)
                        time.sleep(0.2)
                        self.go_up_ahead_platform()
                        self.controller.move_cmd(800, 800)
                        time.sleep(0.8)
                        self.default_platform()
                        self.controller.move_cmd(800, 800)
                        time.sleep(0.4)
                        self.controller.move_cmd(0, 0)
                        time.sleep(0.1)
                    else:
                        time.sleep(0.02)
                # elif edge == 102:
                    # self.controller.move_cmd(800, 800)
                    # time.sleep(0.01)
            # 搁浅左侧在擂台右侧在地面
            if stage == 3:
                print("左高右低")
                self.na += 1
                if self.na == 350:
                    self.controller.move_cmd(-800, 800)
                    self.controller.up.CDS_SetAngle(5, 1000, self.servo_speed)
                    self.controller.up.CDS_SetAngle(7, 24, self.servo_speed)
                    time.sleep(0.8)
                    self.default_platform()
                    time.sleep(0.6)
                    self.na = 0
                else:
                    time.sleep(0.001)
            # 搁浅右侧在擂台左侧在地面
            if stage == 4:
                print("右高左低")
                self.na += 1
                if self.na == 350:
                    self.controller.move_cmd(800, -800)
                    self.controller.up.CDS_SetAngle(6, 24, self.servo_speed)
                    self.controller.up.CDS_SetAngle(8, 1000, self.servo_speed)
                    time.sleep(0.8)
                    self.default_platform()
                    time.sleep(0.6)
                    self.na = 0
                else:
                    time.sleep(0.001)
                
            if stage == 5:
                print("已浮空")
                self.pack_up_ahead()
                self.pack_up_behind()
                self.controller.move_cmd(-800,-800)
                time.sleep(1)
                self.controller.move_cmd(0,0)
                time.sleep(0.5)
                self.controller.move_cmd(800,-800)
                time.sleep(0.5)
                self.default_platform()

if __name__ == '__main__':
    match_demo = MatchDemo()
    # match_demo.stop()
    match_demo.start_match()
