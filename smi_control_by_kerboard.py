import uptech
import time
import up_controller

def stop():
    up.CDS_SetSpeed(1,0)
    up.CDS_SetSpeed(2,0)

def move_up():
    up.CDS_SetSpeed(1,512)
    up.CDS_SetSpeed(2,-512)

def move_back():
    up.CDS_SetSpeed(1,-512)
    up.CDS_SetSpeed(2,512)

def move_rotation_right():
    up.CDS_SetSpeed(1,512)
    up.CDS_SetSpeed(2,512)
    
def move_rotation_left():
    up.CDS_SetSpeed(1,-512)
    up.CDS_SetSpeed(2,-512)

def move_right():
    up.CDS_SetSpeed(1,512)
    up.CDS_SetSpeed(2,0)

def move_left():
    up.CDS_SetSpeed(1,0)
    up.CDS_SetSpeed(2,-512)

if __name__ == '__main__':
    up=uptech.UpTech()
    up.CDS_Open()
    up.CDS_SetMode(1,1)
    up.CDS_SetMode(2,1)
    while True:
        key = input("get word:")
           
        if key == 's':
            stop()
            time.sleep(0.3)
            move_back()
        elif key == 'w':
            stop()
            time.sleep(0.3)
            move_up()
        elif key == 'a':
            stop()
            time.sleep(0.3)
            move_rotation_left() 
        elif key == 'd':
            stop()
            time.sleep(0.3)
            move_rotation_right()
        elif key == 'q':
            stop()
            time.sleep(0.3)
            move_left()
        elif key == 'e':
            stop()
            time.sleep(0.3)
            move_right()
        elif key == 'z':
            stop()