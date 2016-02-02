#!/usr/bin/python3
import requests

class WorldLink:
    
    loginUrl = "https://ssl.worldlink.com.np:444/eservice/index.php/login/processLogin"
    ticketUrl = "https://ssl.worldlink.com.np:444/eservice/support/ticket_submit"

    def __init__(self, username, password):
        self.session = requests.Session()
        self.username = username
        login = self.session.post(self.loginUrl, data = {'username': username, 'password': password})
        if "/log/" in login.headers.get('refresh'):
            self.loggedIn = True
        else:
            print("Failed to login! Please make sure username/password are correct.")
            self.loggedIn = False

    def reportTicket(self, message):
        print("Message: "+ message)
        if self.loggedIn:
            data = self.session.post(self.ticketUrl, data = {'problem_type_name': 11, 'problem_types': 256, 'additional_info': message })
            if "Ticket ID" in data.text:
                print("Ticket Created Successfully!")
            else:
                print("There was a problem creating the ticket.")
        else:
            return None