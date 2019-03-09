import time
import socket
from AMSpi import AMSpi

leftCount = 0
rightCount = 0
backwardCount = 0
forwardCount = 0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Socket Created"
#imports libraries

ip= '10.202.2.19'
#ip= '10.0.0.188'
#gives static ip for the server (change for your wifi networks)
port = 2345
#randomly assign a specific frequency for your program you want to send
address = (ip, port)
#gives port and ip synced together
server.bind(address)
#permantly bind to specific ip and port

server.listen(2)
#amount of clinets you want to listen to

client, addr = server.accept()

if __name__ == '__main__':
    # Calling AMSpi() we will use default pin numbering: BCM (use GPIO numbers)
    # if you want to use BOARD numbering do this: "with AMSpi(True) as amspi:"
        with AMSpi() as amspi:

            # Set PINs for controlling shift register (GPIO numbering)
            amspi.set_74HC595_pins(21, 20, 16)
            # Set PINs for controlling all 4 motors (GPIO numbering)
            amspi.set_L293D_pins(PWM2A=13, PWM2B=19)

            while True:
                    command = client.recv(1024)
                    #listen for commands from mac
                    #1024 converts binary to words
                    print command
                    #prints the command that was recieved

                    
                    if command == "Forward":
                        if (forwardCount == 0):
                                amspi.run_dc_motors([amspi.DC_Motor_1], speed=75, clockwise=True)
                                forwardCount = 1 + forwardCount
                        
                        
                    if command == "Right":
                        if (rightCount == 0):
                                amspi.run_dc_motors([amspi.DC_Motor_2])
                                amspi.run_dc_motors([amspi.DC_Motor_1], speed=75, clockwise=True)
                                rightCount = 1 + rightCount

                    if command == "Left":
                        if (leftCount == 0):
                                amspi.run_dc_motors([amspi.DC_Motor_2], clockwise=False)
                                amspi.run_dc_motors([amspi.DC_Motor_1], speed=75, clockwise=True)
                                leftCount = 1 + leftCount

                    if command == "Backwards":
                        if (backwardCount == 0):
                                amspi.run_dc_motors([amspi.DC_Motor_1], speed=75, clockwise=False)
                                backwardCount = 1 + backwardCount

                    if command == "Brake":
                        amspi.stop_dc_motors([amspi.DC_Motor_2, amspi.DC_Motor_1])
                        amspi.run_dc_motors([amspi.DC_Motor_2])
                        amspi.stop_dc_motors([amspi.DC_Motor_2, amspi.DC_Motor_1])
                        forwardCount = 0
                        rightCount = 0
                        leftCount = 0
                        backwardCount = 0 
                        time.sleep(1)
        
