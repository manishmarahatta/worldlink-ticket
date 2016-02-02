#!/usr/bin/python3
import os, sys, csv, datetime, re
from WorldLink import WorldLink

# Worldlink's Username
username="yourUsernameHere"
# Worldlink's Password
password="yourPasswordHere"

# Do you want to save the speed tests to a file?
logData=True
# Where do you want to save it?
logFile="/home/pi/worldlink-log.csv"

# If internet drops below downloadThreshold Mbps
# A ticket is issued with worldlink
downloadTheshold = 18

# Message for the trouble ticket
message = "I am subscribed to 25Mbps plan but my current internet speed is {download}Mbps Download and {upload}Mbps Upload. Fix this ASAP."

def speedtest(server):
        print('Running test at Server#' + str(server))
        speed = os.popen("speedtest-cli --simple --server " + str(server)).read()
        if speed == "":
                print("Seems like you havent installed speedtest-cli")
                print("To install it, run the command: sudo apt-get install speedtest-cli")
                exit()
        print(speed)
        date = str(datetime.datetime.now())
        if "Cannot" in speed:
                data = [server, 0, 0, 0, date]
        else:
                fSpeed= re.search('(?:Ping: )([0-9.]+)(?: ms)(?:\n)(?:Download: )([0-9.]+)(?: Mbits\/s)(?:\n)(?:Upload: )([0-9.]+)(?: Mbits\/s)', speed)
                data = [ server, float(fSpeed.group(1)), float(fSpeed.group(2)), float(fSpeed.group(3)), date]
        if logData:
                save(data)
        return data

def save(data):
        target = open(logFile, 'a')
        writer = csv.writer(target)
        writer.writerow((data[0], data[4], data[1], data[2], data[3]))
        target.close()

def average(speed1, speed2, speed3):
        return [ ( (speed1[2] + speed2[2] + speed3[2]) / 3 ), ( (speed1[3] + speed2[3] + speed3[3]) / 3 )]

def test():
        # Run the speedtest on 3 different servers and calculate the average speed
        averageDownload, averageUpload = average(speedtest(4098), speedtest(4153), speedtest(6405))
        print("Average Download Speed:" + str(averageDownload))
        print("Average Upload Speed:" + str(averageUpload))
        if averageDownload < downloadTheshold:
                print("Trying to Report Ticket")
                worldlink = WorldLink(username, password)
                worldlink.reportTicket(message.format(download=averageDownload, upload=averageUpload))
        else:
                print("Awesome!! Internet Speed is fine!! No need to report ticket!!")

if __name__ == '__main__':
        test()