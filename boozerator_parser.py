import serial

def scan_for_chars():
    ser = serial.Serial('COM10', timeout=5)
    while(1):
        header1 = ord(ser.read()) # first header
        if header1 == 85: 
            header2 = ord(ser.read()) # second header
            if header2 == 85: 
                length = ord(ser.read()) # length
                frametype = ord(ser.read()) # frame type
                if frametype == 1: # make sure it's a temp data frame
                    temp1_upper = ord(ser.read())
                    temp1_lower = ord(ser.read())
                    temp2_upper = ord(ser.read())
                    temp2_lower = ord(ser.read())
                    checksum = ord(ser.read())
                    
                    # calc checksum
                    check_total = (header1+header2+length+frametype+temp1_upper+temp1_lower+temp2_upper+temp2_lower+checksum) & 0xFF
                    if check_total == 255:
                        # If packet is good, convert the temps
                        temp1_c = (temp1_lower + (temp1_upper << 8))*0.0625
                        temp1_f = temp1_c *1.8 + 32.0
                        temp2_c = (temp2_lower + (temp2_upper << 8))*0.0625
                        temp2_f = temp2_c *1.8 + 32.0

                        print "temp1: ", temp1_f, "\n"
                        #print "temp1: ", temp2_f, "\n"
                    else:
                        print "Invalid checksum\n"
                    
