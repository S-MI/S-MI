import uptech
import time



up=uptech.UpTech()

up.LCD_Open(2)
up.ADC_IO_Open()
#up.ADC_Led_SetColor(0,0x2F0000)
#up.ADC_Led_SetColor(1,0x002F00)
up.CDS_Open()
up.CDS_SetMode(1,0)
up.CDS_SetMode(6,0)
up.MPU6500_Open()

up.LCD_PutString(120, 0, 'lcdtest')
up.LCD_Refresh()
up.LCD_SetFont(up.FONT_6X10)




count=0
sign=0
io_data = []



while True:
           
    adc_value=up.ADC_Get_All_Channle()
    #print(adc_value)
    
    #get_battry_voltage--------------------------------------------------------------------------------------------
    battery_voltage_float = adc_value[9]*3.3*4.0/4096
    str_battery_voltage_float='%.2fV' % battery_voltage_float
    print(str_battery_voltage_float)

    up.LCD_PutString(0,16,'Battery:'+str_battery_voltage_float+'  ')
    #print(str_battery_voltage_float)
    #end-----------------------------------------------------------------------------------------------------------
    
    #get_MPU_value-------------------------------------------------------------------------------------------------
    attitude=up.MPU6500_GetAttitude()   
    str_attitude_pitch='Pitch:%.2f  ' % attitude[0]
    str_attitude_roll='Roll :%.2f  ' % attitude[1]
    str_attitude_yaw='Yaw  :%.2f  ' % attitude[2]

    up.LCD_PutString(0,30,str_attitude_pitch)
    up.LCD_PutString(0,44,str_attitude_roll)
    up.LCD_PutString(0,58,str_attitude_yaw)
    up.LCD_Refresh()
    #end-----------------------------------------------------------------------------------------------------------


    io_all_input = up.ADC_IO_GetAllInputLevel()
    io_array = '{:08b}'.format(io_all_input)
    io_data.clear()


    for index, value in enumerate(io_array):       
        io = (int)(value)     
        io_data.insert(0,io)  
      #?
    print("adc_value : {}".format(adc_value))
    print("io_value : {}".format(io_data))

    if count >= 10:
        if sign != 0:
            up.CDS_SetAngle(1,0,250)
            up.ADC_Led_SetColor(1,0x2F0000)
            up.ADC_Led_SetColor(0,0x001F)
            time.sleep(1)                  
            sign = 0
        else:
            up.CDS_SetAngle(1,512,250)
            up.ADC_Led_SetColor(0,0x2F0000)
            up.ADC_Led_SetColor(1,0x002F00)
            sign = 1
        count = 0
    else:
        count += 1 

    time.sleep(0.1)
        
  
        
    



