#!/usr/bin/env python3.0
#Hourly Tempterature, Air Pressure, and Humidity Logger
#6/18/2025 by Evan Hill & Tim Ledesma 

import time
import csv
import smbus2
import bme280
#sudo apt install python3-RPi.bme280
#sudo mv /usr/lib/python3.11/EXTERNALLY-MANAGED /usr/lib/python3.11/EXTERNALLYMANAGED.bak
#sudo pip install RPI.BME280
import datetime

counter = -1

# BME280 sensor address (default address)
address = 0x77

# Initialize I2C bus
bus = smbus2.SMBus(1)

# Load calibration parameters
calibration_params = bme280.load_calibration_params(bus, address)

# Labels for csv file
labels = [
    ['Date', 'Time', 'Temp', 'Pressure', 'Humidity']
]

# File path for the CSV file
file_path = 'templog.csv'

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def hPa_to_inHg(hPa):
    return 29.92 * (hPa / 1013.2)

def add(counter):
    return 1+ counter

def write_to_file(counter, current_date, current_time, temperature_celsius, press_conv, humidity):
    values = [
    [current_date, current_time, temperature_celsius, press_conv, humidity]
    ]
    if counter == 0:
        with open(file_path, 'a', newline='') as file:
            # Create a CSV writer object
            writer = csv.writer(file)

            # Write multiple rows at once
            writer.writerows(labels)
            writer.writerows(values)
    else:
        with open(file_path, 'a', newline='') as file:
            # values for csv file

            # Create a CSV writer object
            writer = csv.writer(file)

            # Write multiple rows at once
            writer.writerows(values)

        
##    with open('templog.txt', 'a') as f:
##            time = str(current_time)
##            f.write(time+"\n")
##            temp = round(temperature_celsius, 2)
##            temp = str(temp)
##            f.write("Temperature: "+temp+"°C"+"\n")
##            inHg = round(press_conv, 2)
##            inHg = str(inHg)
##            f.write("Pressure: "+inHg+"inHg"+"\n")
##            hum = round(humidity, 2)
##            hum = str(hum)
##            f.write("Humiditiy: "+hum+"%"+"\n"+"\n")
    

while True:
    try:
        # Read sensor data
        data = bme280.sample(bus, address, calibration_params)

        # Extract temperature, pressure, and humidity
        temperature_celsius = data.temperature
        pressure = data.pressure
        humidity = data.humidity
        now = datetime.datetime.now()
        current_date = now.strftime("%m/%d/%Y")
        current_time = now.strftime("%H:%M:%S")

        # Convert temperature to Fahrenheit
        temperature_fahrenheit = celsius_to_fahrenheit(temperature_celsius)
        press_conv = hPa_to_inHg(pressure)
        counter +=1


        # Print the readings
##        print(counter)
        print(current_date)
        print(current_time)
        print("Temperature: {:.2f} °C, {:.2f} °F".format(temperature_celsius, temperature_fahrenheit))
        print("Pressure: {:.2f} inHg".format(press_conv))
        print("Humidity: {:.2f} %".format(humidity))
        write_to_file(counter, current_date, current_time, temperature_celsius, press_conv, humidity)
        

        # Wait for a few seconds before the next reading
        time.sleep(900)

    except KeyboardInterrupt:
        print('Program stopped')
        break
    except Exception as e:
        print('An unexpected error occurred:', str(e))
        break
