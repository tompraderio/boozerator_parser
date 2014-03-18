import serial

def scan_for_chars():
    ser = serial.Serial('COM10', timeout=20)
    while(1):
        header1 = ord(ser.read()) # first header
        if header1 == 85: 
            header2 = ord(ser.read()) # second header
            if header2 == 85: 
                length = ord(ser.read()) # length
                frametype = ord(ser.read()) # frame type
                if frametype == 1: # check the frame type
                    process_temp_frame(ser)
                elif frametype == 2:
                    process_state_frame(ser)
                else:
                    print "Invalid frame type\n"
                    
                    
def process_temp_frame(ser):
    temp0_upper = ord(ser.read())
    temp0_lower = ord(ser.read())
    temp1_upper = ord(ser.read())
    temp1_lower = ord(ser.read())
    temp2_upper = ord(ser.read())
    temp2_lower = ord(ser.read())
    temp3_upper = ord(ser.read())
    temp3_lower = ord(ser.read())
    temp4_upper = ord(ser.read())
    temp4_lower = ord(ser.read())
    temp5_upper = ord(ser.read())
    temp5_lower = ord(ser.read())
    checksum = ord(ser.read())

    # calc checksum
    check_total = (85+85+17+1+temp0_upper+temp0_lower+temp1_upper+temp1_lower+temp2_upper+temp2_lower+temp3_upper+temp3_lower+temp4_upper+temp4_lower+temp5_upper+temp5_lower+checksum) & 0xFF
    if check_total == 255: # If packet is good, convert the temps
        temp0_raw = temp0_lower + (temp0_upper << 8)
        temp1_raw = temp1_lower + (temp1_upper << 8)
        temp2_raw = temp2_lower + (temp2_upper << 8)
        temp3_raw = temp3_lower + (temp3_upper << 8)
        temp4_raw = temp4_lower + (temp4_upper << 8)
        temp5_raw = temp5_lower + (temp5_upper << 8)

        
        # make sure the sensors are connected
        if temp0_raw != 65535:
            #check sign
            if temp0_raw > 32767:
                temp0_c = (0-(-temp0_raw & 65535))*0.0625
            else:
                temp0_c = temp0_raw*0.0625
            
            temp0_f = temp0_c *1.8 + 32.0
            print "temp0: ", temp0_f, "\n"
        else:
            print "temp0: Not Connected\n"

        if temp1_raw != 65535:
            if temp1_raw > 32767:
                temp1_c = (0-(-temp1_raw & 65535))*0.0625
            else:
                temp1_c = temp1_raw*0.0625
            temp1_f = temp1_c *1.8 + 32.0
            print "temp1: ", temp1_f, "\n"
        else:
            print "temp1: Not Connected\n"

        if temp2_raw != 65535:
            temp2_c = temp2_raw*0.0625
            temp2_f = temp2_c *1.8 + 32.0
            print "temp2: ", temp2_f, "\n"
        else:
            print "temp2: Not Connected\n"

        if temp3_raw != 65535:
            temp3_c = temp3_raw*0.0625
            temp3_f = temp3_c *1.8 + 32.0
            print "temp3: ", temp3_f, "\n"
        else:
            print "temp3: Not Connected\n"

        if temp4_raw != 65535:
            temp4_c = temp4_raw*0.0625
            temp4_f = temp4_c *1.8 + 32.0
            print "temp4: ", temp4_f, "\n"
        else:
            print "temp4: Not Connected\n"

        if temp5_raw != 65535:
            temp5_c = temp5_raw*0.0625
            temp5_f = temp5_c *1.8 + 32.0
            print "temp5: ", temp5_f, "\n"
        else:
            print "temp5: Not Connected\n"

        print '\n'
    else:
        print "Invalid checksum\n"

        

def process_state_frame(ser):
    fridge_state = ord(ser.read())
    freezer_state = ord(ser.read())
    checksum = ord(ser.read())
    # calc checksum
    check_total = (85+85+7+2+fridge_state+freezer_state+checksum) & 0xFF
    if check_total == 255:
        print "State frame received\n"
        if fridge_state == 0:
            print "Fridge off\n"
        elif fridge_state == 1:
            print "Fridge low\n"
        elif fridge_state == 9:
            print "Fridge high\n"
        else:
            print "Fridge invalid state\n"

        if freezer_state == 0:
            print "Freezer off\n"
        elif freezer_state == 1:
            print "Freezer low\n"
        elif freezer_state == 9:
            print "Freezer high\n"
        else:
            print "Freezer invalid state\n"

        print "\n"
        
    else:
        print "Invalid checksum\n"
