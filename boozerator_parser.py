import serial
import time

C_HEADER_1 = ord('U')
C_HEADER_2 = ord('U')
C_TEMP_PACKET_TYPE = 1
C_STATE_PACKET_TYPE = 2

def listen_for_packets(com_port):
    ser = serial.Serial(com_port, timeout=40)
    while(1): # Sit on the com port and watch for packet headers
        header1 = ord(ser.read()) # first header
        if header1 == 85: 
            header2 = ord(ser.read()) # second header
            if header2 == 85: 
                # grab the packet's length
                length = ord(ser.read())

                # start buffering the packet
                packet_buf = []
                packet_buf.append(header1)
                packet_buf.append(header2)
                packet_buf.append(length)

                # Buffer the rest of the characters
                for i in range(length-3):
                    packet_buf.append(ord(ser.read()))

                # Checksum the packet
                check_total = 0
                for i in packet_buf:
                    check_total = check_total + i
                if (check_total & 0xFF) == 255:
                    
                    # Handle packet types
                    frametype = packet_buf[3]
                    packet_payload = packet_buf[4:len(packet_buf)-1]
                    if frametype == C_TEMP_PACKET_TYPE:
                        process_temp_frame(packet_payload)
                    elif frametype == C_STATE_PACKET_TYPE:
                        process_state_frame(packet_payload)
                    else:
                        # Error: packet type not supported
                        print "Bad packet type"
                else:
                    # Error: bad checksum
                    print "Bad checksum"
                    
                    
def process_temp_frame(payload):
    temp0_upper = payload[0]
    temp0_lower = payload[1]
    temp1_upper = payload[2]
    temp1_lower = payload[3]
    temp2_upper = payload[4]
    temp2_lower = payload[5]
    temp3_upper = payload[6]
    temp3_lower = payload[7]
    temp4_upper = payload[8]
    temp4_lower = payload[9]
    temp5_upper = payload[10]
    temp5_lower = payload[11]

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
    

def process_state_frame(payload):
    fridge_state = payload[0]
    freezer_state = payload[1]
    
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
