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

# Speedtest.net servers to test on
servers = [ 4098, 4153, 6405 ]

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

def test():
        downloadSpeeds = []
        uploadSpeeds = []
        # Run the speedtest on provided servers
        for server in servers:
                speed = speedtest(server)
                downloadSpeeds.append(speed[1])
                uploadSpeeds.append(speed[2])
        # Calculate the average download speed
        averageDownload = float(sum(downloadSpeeds) / len(downloadSpeeds))
        averageUpload = float(sum(uploadSpeeds) / len(uploadSpeeds))
        print("Average Download Speed:" + str(averageDownload))
        print("Average Upload Speed:" + str(averageUpload))
        if averageDownload < downloadTheshold:
                print("Trying to Report Ticket")
                worldlink = WorldLink(username, password)
                worldlink.reportTicket(message.format(download=round(averageDownload, 3), upload=round(averageUpload, 3)))
        else:
                print("Awesome!! Internet Speed is fine!! No need to report ticket!!")

if __name__ == '__main__':
        test()