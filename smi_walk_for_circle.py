import uptech
import time


def stop():
    up.CDS_SetSpeed(3,0)
    up.CDS_SetSpeed(4,0)

def move_up():
    up.CDS_SetSpeed(3,1023)
    up.CDS_SetSpeed(4,-1023)

def move_back():
    up.CDS_SetSpeed(3,-1023)
    up.CDS_SetSpeed(4,1023)

def move_rotation_right():
    up.CDS_SetSpeed(3,1023)
    up.CDS_SetSpeed(4,1023)
    
def move_rotation_left():
    up.CDS_SetSpeed(3,-1023)
    up.CDS_SetSpeed(4,-1023)

def move_right():
    up.CDS_SetSpeed(3,1023)
    up.CDS_SetSpeed(4,0)

def move_left():
    up.CDS_SetSpeed(3,0)
    up.CDS_SetSpeed(4,-1023)

obstacle = 0
no_obstacle = 1

if __name__ == '__main__':
    up=uptech.UpTech()
    
    up.CDS_Open()
    up.CDS_SetMode(3,1)
    up.CDS_SetMode(4,1)
    up.ADC_IO_Open()
    io_data=[]
    
    while(1):
        io_all_input = up.ADC_IO_GetAllInputLevel()    #get the decimal value corresponding to all io ports.   such as: 11111111->255  11111110->254 ...  
        io_array = '{:08b}'.format(io_all_input)     #Decompose decimal numbers into binary numbers.  such as: 255->11111111 254->11111110
        #print(io_all_input)
        #print(io_array)
        io_data.clear()
        for index, value in enumerate(io_array):       
            io = (int)(value)
            io_data.insert(0,io)
        print(io_data)
        if io_data[0] == obstacle:
            stop()
        elif io_data[0] == no_obstacle and io_data[1] == no_obstacle and io_data[2] == no_obstacle and io_data[3] == no_obstacle:     #no obstacle
            move_up()
            #stop()
            #time.sleep(0.3)
        elif io_data[0] == no_obstacle and io_data[3] == obstacle and io_data[1] == no_obstacle and io_data[2] == no_obstacle:     #right obstacle
            while(1):
                move_rotation_right()
                if io_data[0] == obstacle and io_data[3] == no_obstacle and io_data[1] == no_obstacle and io_data[2] == no_obstacle:
                    break
        elif io_data[0] == no_obstacle and io_data[3] == no_obstacle and io_data[1] == no_obstacle and io_data[2] == obstacle:     #left obstacle
            while(1):
                move_rotation_left()
                if io_data[0] == obstacle and io_data[3] == no_obstacle and io_data[1] == no_obstacle and io_data[2] == no_obstacle:
                    break