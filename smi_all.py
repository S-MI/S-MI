import match_demo
import uptech
import time
def stop():
    up.CDS_SetSpeed(1,0)
    up.CDS_SetSpeed(2,0)

def move_up():
    up.CDS_SetSpeed(1,512)
    up.CDS_SetSpeed(2,-512)

def move_up_right():
    up.CDS_SetSpeed(1,1023)
    up.CDS_SetSpeed(2,-512)

def move_up_fastest():
    up.CDS_SetSpeed(1,1023)
    up.CDS_SetSpeed(2,-1023)

def move_back():
    up.CDS_SetSpeed(1,-512)
    up.CDS_SetSpeed(2,512)
    
def move_back_right():
    up.CDS_SetSpeed(1,-512)
    up.CDS_SetSpeed(2,1023)
    
def move_back_left():
    up.CDS_SetSpeed(1,-1023)
    up.CDS_SetSpeed(2,512)

def move_right():
    up.CDS_SetSpeed(1,800)
    up.CDS_SetSpeed(2,0)

def move_rotation_right():
    up.CDS_SetSpeed(1,800)
    up.CDS_SetSpeed(2,800)

def move_right_back():
    up.CDS_SetSpeed(1,0)
    up.CDS_SetSpeed(2,800)

def move_left():
    up.CDS_SetSpeed(1,0)
    up.CDS_SetSpeed(2,-800)
    
def move_rotation_left():
    print("left_ok")
    up.CDS_SetSpeed(1,-800)
    up.CDS_SetSpeed(2,-800)
    
def move_left_back():
    up.CDS_SetSpeed(1,-800)
    up.CDS_SetSpeed(2,0)

if __name__ == "__main__":
    MyRobot = match_demo.MatchDemo()
    up = uptech.UpTech()
    
    
    MyRobot.default_platform()
    #MyRobot.default_platform()
    
    #MyRobot.go_up_ahead_platform()
    #MyRobot.go_up_behind_platform()

    up.CDS_Open()
    up.CDS_SetMode(1,1)
    up.CDS_SetMode(2,1)
    up.ADC_Led_SetColor(1,0x0000)
    
    #MyRobot.start_match()
    
    #move_up()
    
    while(1):
        ## 底部前方红外光电
        #ad1 = MyRobot.controller.adc_data[5]
        ## 底部右侧红外光电
        #ad2 = MyRobot.controller.adc_data[8]
        ## 底部后方红外光电
        #ad3 = MyRobot.controller.adc_data[6]
        ## 底部左侧红外光电
        #ad4 = MyRobot.controller.adc_data[7]
        
        #ad5 = MyRobot.controller.adc_data[0]
        
        #key_down = MyRobot.enemy_detect()
        key_up = MyRobot.edge_detect()
        print(key_up)
        print(MyRobot.controller.io_data)
        #print('ad1',"                        ",ad1)
        ##print("                        ",key_down)
        #if key_down == 0:
        #    move_up()
        #    print("barrier_free")
        #elif key_down == 1 or key_down == 11:
        #    stop()
        #    time.sleep(1)
        #    print("barrier_front")
        #    #move_back()
        #elif key_down == 2 or key_down == 3:
        #    print("barrier_right_or_back")
        #    stop()
        #    time.sleep(0.3)
        #    while(1):
        #        ad1 = MyRobot.controller.adc_data[5]    #realtime_update_turnning
        #        move_rotation_right()
        #        if ad1 <= 100:
        #            stop()
        #            time.sleep(1)
        #            break
        #    #move_back()
        #elif key_down == 4:
        #    print("barrier_left")
        #    stop()
        #    time.sleep(0.3)
        #    while(1):
        #        ad1 = MyRobot.controller.adc_data[5]
        #        move_rotation_left()
        #        if ad1 <= 100:
        #            stop()
        #            time.sleep(1)
        #            break
        #    #move_back()
        
        
        #key = MyRobot.edge_detect()
        #print(key)
        if key_up == 0:    #没有检测到边缘
            move_up()
            #time.sleep(0.5)
        elif key_up == 1:    # 左前检测到边缘
            move_back_right()
            time.sleep(0.5)
        elif key_up == 2:    # 右前检测到边缘
            move_back_left()
            time.sleep(0.5)
        elif key_up == 3:    # 右后检测到边缘
            move_left()
            time.sleep(0.5)
        elif key_up == 4:    # 左后检测到边缘
            move_right()
            time.sleep(0.5)
        elif key_up == 5:    # 前方两个检测到边缘
            move_back()  
            time.sleep(1)
        elif key_up == 6:    # 后方两个检测到边缘
            move_up()
            time.sleep(1)
        elif key_up == 7:    # 左侧两个检测到边缘
            move_back_right()
            time.sleep(0.5)
        elif key_up == 8:    # 右侧两个检测到边缘
            move_back_left()
            time.sleep(0.5)
        #elif key == 9:
        #    up.ADC_Led_SetColor(1,0xFFFF)
        #    up.ADC_Led_SetColor(2,0xFFFF)
        #    stop()
            # time.sleep(0.5)
                
        
        
        #MyRobot.default_platform()
        #time.sleep(1)
        #MyRobot.shovel_state()
        #time.sleep(1)
        
        #test servo---------------------------------------------------------
        #print(1)
        #up.CDS_SetAngle(5,300,512)
        #time.sleep(0.7)
        #up.CDS_Setangle(5,650,512)
        #time.sleep(0.7)
