# WorldLink Auto Ticket Reporter

## Overview
This program conducts speedtest with provided speedtest.net servers and creates a ticket with WorldLink Communications if the internet speed is below the specified threshold.

## Requirements
The program uses python 3.
```
sudo apt-get install python3
```

You will need to install `speedtest-cli`
### Install through pip

```python
sudo pip install speedtest-cli
```

### Install through Ubuntu package manager
```
sudo apt-get install speedtest-cli
```

You will also need `requests` package for python3
```
sudo pip install requests
```

Sometimes the pip executable is named differently. You can find the executable name using
```
ls /usr/bin | grep ^pip
```

### Clone this repository
```
git clone https://github.com/nikhil-pandey/worldlink-ticket
```

## Usage
1. Change the variables `username`, `password`, `logData`, `logFile`, `downloadThreshold`, `message`, `servers` according to your needs.
2. Use `{download}` and `{upload}` in `message` to replace with actual speed.
3. Optionally change the `servers` to the server ids from [Speedtest.net Servers](http://www.speedtest.net/speedtest-servers-static.php). You can use as many as you want to calculate an average speed.
4. Give proper permissions to `main.py`. `chmod +x main.py` should be enough.
5. Set a cron job every hour(s)/day(s) according to your choice to run the program `/path/to/main.py`

`Note: If you are on a volume based plan, running this might finish some of your data.`

## License
This package is open-sourced software licensed under the [MIT license](http://opensource.org/licenses/MIT)