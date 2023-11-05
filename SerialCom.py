import serial
import serial.tools.list_ports

def findArduino():
    arduino_ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if 'Arduino' in p.description or 'VID:PID=2341:8054' in p.hwid
    ]

    if not arduino_ports:
        print("No Arduino found. Check the connection and try again.")
        return None
    elif len(arduino_ports) > 1:
        print("Multiple Arduinos found. Please unplug the extras.")
        return None
    else:
        print(f"Arduino found at {arduino_ports[0]}")
        return arduino_ports[0]


def SendInfo(sendData):

    comPort = findArduino()

    if comPort != None:
        # Establish a serial connection (adjust port and baud rate as needed)
        ser = serial.Serial(comPort, 9600)

        # Send data to Arduino
        data_to_send = sendData
        ser.write(data_to_send.encode())

        # Close the serial connection
        ser.close()