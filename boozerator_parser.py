import serial
import time

def scan_for_chars():
    ser = serial.Serial('COM10', timeout=40)
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
        temps_raw = [temp0_lower + (temp0_upper << 8)]
        temps_raw.append(temp1_lower + (temp1_upper << 8))
        temps_raw.append(temp2_lower + (temp2_upper << 8))
        temps_raw.append(temp3_lower + (temp3_upper << 8))
        temps_raw.append(temp4_lower + (temp4_upper << 8))
        temps_raw.append(temp5_lower + (temp5_upper << 8))

        temps_c = [0] * len(temps_raw)
        temps_f = [0] * len(temps_raw)
        
        # make sure the sensors are connected
        for i in range(len(temps_raw)):
            if temps_raw[i] != 65535:
                #check sign
                if temps_raw[i] > 32767:
                    temps_c[i] = (0-(-temps_raw[i] & 65535)) * 0.0625
                else:
                    temps_c[i] = temps_raw[i] * 0.0625
                
                temps_f[i] = temps_c[i] * 1.8 + 32.0
                print "temp"+str(i)+": ", temps_f[i], "\n"
            else:
                temps_f[i] = 0.0
                print "temp"+str(i)+": Not Connected\n"        

        # log the temps
        f = open('temps.log','a')
        f.write(time.strftime("%c") + ',')
        for i in range(len(temps_f)):
            f.write(str(temps_f[i])+',')
        f.write('\n')
        f.close()
        
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
