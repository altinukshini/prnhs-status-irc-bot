#!/usr/bin/python

import socket
import time
import requests
import json
from requests.auth import HTTPBasicAuth

SELTZERSERVER = "www.yourdomain.com"
HTACCESSUSER = "USERNAME"
HTACCESSPASSWD = "PASSWORD"

def getStatus():
    url = 'http://' + SELTZERSERVER + '/crm/api/query.php?action=hackerspaceStatus'
    payload = ''
    response = requests.get(url, auth=HTTPBasicAuth(HTACCESSUSER, HTACCESSPASSWD),data=payload, timeout=30.0)

    status = json.loads(response.content)

    return status

server = "irc.freenode.net"
channels = ["#altin", "#flossk"]
botnick = "PRNHS"

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "connecting to:" + server
irc.connect((server, 6667))
irc.send("USER "+ botnick + " " + botnick + " " + botnick + " :Prishtina Hackerspace | Hackerspace status bot.\n")
irc.send("NICK "+ botnick +"\n")
irc.send("PRIVMSG nickserv :iNOOPE\r\n")
irc.send("JOIN " + ",".join(channels) + "\n")

while 1:
   text=irc.recv(2040)
   print text

   statusJson = getStatus()
   hackersInSpace = statusJson['hackersInSpace']
   message = statusJson['message']
   memberNames = statusJson['memberNames']

   for index, channel in enumerate(channels):

       if text.find('PING') != -1:
          irc.send('PONG ' + text.split() [1] + '\r\n')

       if text.find(channel + ' :!hi') !=-1:
          irc.send('PRIVMSG ' + channel + ' :Hello! \r\n')

       if text.find(channel + ' :!prnhs') !=-1:
          irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')

       if text.find(channel + ' :!who') !=-1:
          irc.send('PRIVMSG ' + channel + ' :Hackers in space: ' + memberNames + '\r\n')

       if text.find(channel + ' :!status') !=-1:
          if hackersInSpace > 0:
              irc.send('PRIVMSG ' + channel + ' :Prishtina Hackerspace is OPEN\r\n')
          else:
              irc.send('PRIVMSG ' + channel + ' :Prishtina Hackerspace is CLOSED\r\n')

       if text.find(channel + ' :!help') !=-1:
          irc.send('PRIVMSG ' + channel + ' :Use: ![help, status, who, prnhs]\r\n')

       if text.find(channel + ' :PRNHS help') !=-1:
          irc.send('PRIVMSG ' + channel + ' :Use: ![help, status, who, prnhs]\r\n')


   time.sleep(2)
