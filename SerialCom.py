import serial

# Establish a serial connection (adjust port and baud rate as needed)
ser = serial.Serial('COM3', 9600)

# Send data to Arduino
data_to_send = 'Hello Arduino!'
ser.write(data_to_send.encode())

# Close the serial connection
ser.close()