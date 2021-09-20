#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uptech
import time
import up_controller

def stop():
    up.CDS_SetSpeed(1,0)
    up.CDS_SetSpeed(2,0)

def move_up():
    up.CDS_SetSpeed(1,800)
    up.CDS_SetSpeed(2,-800)

def move_up_highspeed():
    up.CDS_SetSpeed(1,1023)
    up.CDS_SetSpeed(2,-1023)

def move_back():
    up.CDS_SetSpeed(1,-800)
    up.CDS_SetSpeed(2,800)

def move_rotation_right():
    up.CDS_SetSpeed(1,1023)
    up.CDS_SetSpeed(2,1023)
    
def move_rotation_left():
    up.CDS_SetSpeed(1,-800)
    up.CDS_SetSpeed(2,-800)

def move_right():
    up.CDS_SetSpeed(1,800)
    up.CDS_SetSpeed(2,0)

def move_right_back():
    up.CDS_SetSpeed(1,0)
    up.CDS_SetSpeed(2,800)

def move_left():
    up.CDS_SetSpeed(1,0)
    up.CDS_SetSpeed(2,-800)
    
def move_left_back():
    up.CDS_SetSpeed(1,-800)
    up.CDS_SetSpeed(2,0)

if __name__ == '__main__':
    up=uptech.UpTech()
    
    #up.ADC_IO_Open()
    #up.ADC_Led_SetColor(0,0x0000)
    #up.ADC_Led_SetColor(1,0x0000)
    #io_data = []
    
    #up.LCD_Open(3)
    #up.LCD_SetFont(up.FONT_7X12) #set 5th for font
    #up.LCD_SetForeColor(up.COLOR_WHITE)
    #up.LCD_SetBackColor(up.COLOR_GREEN)
    #up.LCD_FillScreen(up.COLOR_GREEN)
    #up.LCD_FillFrame(0,0,20,20,up.COLOR_BLACK)
    #up.LCD_FillRoundFrame(0,20,40,50,10,up.COLOR_BRED)
    #up.LCD_DrawMesh(0,0,100,100,up.COLOR_BLUE)
    #up.LCD_DrawFrame(0,0,100,100,up.COLOR_BLUE)
    #for i in range(0,50):
    #    for j in range(0,50):
    #        up.LCD_DrawPixel(i,j,up.COLOR_WHITE)
    #up.LCD_DrawArc(50,50,100,10,up.COLOR_BRED)
    
    up.CDS_Open()
    up.CDS_SetMode(1,1)
    up.CDS_SetMode(2,1)
    up.CDS_SetMode(5,0)
    up.CDS_SetMode(6,0)
    up.CDS_SetMode(7,0)
    up.CDS_SetMode(8,0)
    while True:
        
        #up.CDS_SetAngle(5,650,512)
        #up.CDS_SetAngle(6,650,512)
        #up.CDS_SetAngle(7,300,512)
        #up.CDS_SetAngle(8,300,512)
        #time.sleep(3)
        #up.CDS_SetAngle(5,300,512)
        #up.CDS_SetAngle(6,300,512)
        #up.CDS_SetAngle(7,650,512)
        #up.CDS_SetAngle(8,650,512)
        #time.sleep(3)
        
        key = input("get word:")
        #print("put word",key)
        if key == 's':
            stop()
            time.sleep(0.3)
            move_back()
            #time.sleep(0.1)
        elif key == 'w':
            stop()
            time.sleep(0.3)
            move_up()
            #time.sleep(0.1)
        elif key == 'r':
            stop()
            time.sleep(0.3)
            move_up_highspeed()
        elif key == 'a':
            stop()
            time.sleep(0.3)
            move_rotation_left()
            #time.sleep(2)
            #stop()
        elif key == 'd':
            stop()
            time.sleep(0.3)
            move_rotation_right()
            #time.sleep(0.1)
        elif key == 'q':
            stop()
            time.sleep(0.3)
            move_left()
            #time.sleep(0.1)
        elif key == 'e':
            stop()
            time.sleep(0.3)
            move_right()
            #time.sleep(0.1)
        elif key == 'z':
            stop()
            up.CDS_SetAngle(5,650,512)
            up.CDS_SetAngle(6,650,512)
            up.CDS_SetAngle(7,300,512)
            up.CDS_SetAngle(8,300,512)
            #time.sleep(0.1)
        elif key == '1':
            up.CDS_SetAngle(5,300,512)
            up.CDS_SetAngle(7,650,512)
            #time.sleep(1)
        elif key == '2':
            up.CDS_SetAngle(6,300,512)
            up.CDS_SetAngle(8,650,512)
            #time.sleep(1)
        elif key == '3':
            up.CDS_SetAngle(6,300,512)
            up.CDS_SetAngle(7,650,512)
            #time.sleep(1)
        elif key == '4':
            up.CDS_SetAngle(5,300,512)
            up.CDS_SetAngle(8,650,512)
            #time.sleep(1)
                
        
        #io_all_input = up.ADC_IO_GetAllInputLevel()    #get the decimal value corresponding to all io ports.   such as: 11111111->255  11111110->254 ...  
        #io_array = '{:08b}'.format(io_all_input)     #Decompose decimal numbers into binary numbers.  such as: 255->11111111 254->11111110
        ##print(io_all_input)
        ##print(io_array)
        #io_data.clear()
        #for index, value in enumerate(io_array):       
        #    io = (int)(value)
        #    io_data.insert(0,io)
        #print(io_data)
        #if io_data[7]==1:
        #    #print(1)
        #    up.ADC_Led_SetColor(0,0X8430)
        #    up.ADC_Led_SetColor(1,0X8430)
        #    time.sleep(0.2)
        #else:
        ##up.CDS_SetAngle(1,256,800)
        #    #print(0)
        #    up.ADC_Led_SetColor(0,0xF800)
        #    up.ADC_Led_SetColor(1,0xF800)
        ##up.CDS_SetAngle(1,500,256)
        #    time.sleep(0.2)
    
        #print(1)
        #AllInputLevel = up.ADC_IO_GetAllInputLevel()
        #print(AllInputLevel)
        
        
        
        #up.LCD_Refresh()
        #up.LCD_PutString(70,50,"LCD")
        #up.LCD_PutString(86,58,"D")
        
        
        
        
        #up.CDS_SetSpeed(1,1023)
        #up.CDS_SetSpeed(2,-1023)
        
        
        
        
        
        #up.CDS_SetAngle(5,300,512)
        ##time.sleep(1)
        #up.CDS_SetAngle(6,300,512)
        ##time.sleep(1)
        #up.CDS_SetAngle(7,650,512)
        ##time.sleep(1)
        #up.CDS_SetAngle(8,650,512)
        #time.sleep(1)
        #up.CDS_SetAngle(5, 650, 512)
        ##time.sleep(1)    #changed
        #up.CDS_SetAngle(6, 650, 512)
        ##time.sleep(1)
        #up.CDS_SetAngle(7, 300, 512)
        ##time.sleep(1)
        #up.CDS_SetAngle(8, 300, 512)
        #time.sleep(1)
    




