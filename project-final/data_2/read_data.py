import serial
import time
import csv
import pandas as pd

# ser = serial.Serial(
#     port='/dev/tty.usbserial-14430',\
#     baudrate=115200,\
#     parity=serial.PARITY_NONE,\
#     stopbits=serial.STOPBITS_ONE,\
#     bytesize=serial.EIGHTBITS,\
#         timeout=0)

# print("connected to: " + ser.portstr)

# f = open("data.txt", "w")
gesture = 'clockwise_'
count = 10

t_end = time.time() + 1
while time.time() < t_end:
    pass

while True:
    with serial.Serial(port='/dev/tty.usbserial-14330', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0) as ser:
        print(f"Loop: {count}")
        accel_x = []
        accel_y = []
        accel_z = []
        gyro_x = []
        gyro_y = []
        gyro_z = []
        t_end = time.time() + 4
        print("START READING DATA")
        while time.time() < t_end:
            line = ser.readline()
            if line:
                line = line.decode()
                print(line)
                # f.write(str(count) + ", "+ line)
                line = line.replace(' ', '')
                data = line.split(',')
                if len(data) == 6 and data[0] != '':
                    data[5] = data[5].replace('\r\n', '')
                    accel_x.append(float(data[0]))
                    accel_y.append(float(data[1]))
                    accel_z.append(float(data[2]))

                    gyro_x.append(float(data[3]))
                    gyro_y.append(float(data[4]))
                    gyro_z.append(float(data[5]))

        dict = {'accel_x': accel_x, 'accel_y': accel_y, 'accel_z': accel_z, 'gyro_x': gyro_x, 'gyro_y': gyro_y, 'gyro_z': gyro_z}
        df = pd.DataFrame(dict)
        print(len(df))
        df.to_csv(gesture + str(count))
        print(count)
        count += 1
        t_end = time.time() + 2
        while time.time() < t_end:
            pass
    ser.close()
f.close()

# with open('data.txt', 'r') as in_file:
#     stripped = (line.strip() for line in in_file)
#     lines = (line.split(",")[0:4] for line in stripped if line)
#     with open('accel_' + gesture + num + '.csv', 'w') as out_file:
#         writer = csv.writer(out_file)
#         writer.writerow(('sample', 'accel_x', 'accel_y', 'accel_z'))
#         writer.writerows(lines)

# with open('data.txt', 'r') as in_file:
#     stripped = (line.strip() for line in in_file)
#     lines = (line.split(",")[0:1] + line.split(",")[4:] for line in stripped if line)
#     with open('gyro_' + gesture + num + '.csv', 'w') as out_file:
#         writer = csv.writer(out_file)
#         writer.writerow(('sample', 'gyro_x', 'gyro_y', 'gyro_z'))
#         writer.writerows(lines)

    
# ser.close()


