#!/bin/python3.8
import sys
import os
import datetime
import netmiko
import smtplib
from email.message import EmailMessage
from netmiko import SSHDetect, Netmiko
from dotenv import load_dotenv

path = './env'

load_dotenv(dotenv_path=path, verbose=True)
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')

email_username = os.environ.get('EMAIL_USERNAME')
email_password = os.environ.get('EMAIL_PASSWORD')
port = 22
hostname = sys.argv[1]

netmiko_exceptions=(netmiko.ssh_exception.NetMikoTimeoutException,
                   netmiko.ssh_exception.NetMikoAuthenticationException)

device = {
            "device_type": "cisco_ios",
            "host": hostname,
            "username": username,
            "password": password,
            }

command = 'show ip arp'

#Connect to device and get command output
try:
    connect=Netmiko(**device)
    command_output=connect.send_command(command)
    device_name = connect.find_prompt()[:-1]
    connect.disconnect()

except netmiko_exceptions as e:
    print('Failed to device',device["host"], e)


arp_table = f'./{device_name}.arp_table'
arp_table_diff = f'./{device_name}.arp_table_diff'


#Parse the arp table output to include IP, MAC and INTERFACE
arp_entry = []
for output in command_output.splitlines()[1:]:
    output = ' - '.join(output.split()[i] for i in [1,3,5])
    arp_entry.append(output)


#Check if arp_table file exist and compare arp tables from the device, if not create a new arp_table file
if os.path.exists(arp_table):
    
    if open(arp_table,'r').read().splitlines() == arp_entry:
        sys.exit("No arp_table change")
    
    #Compare arp output with arp_table file
    with open(arp_table) as f:
        s = set([line.rstrip('\n') for line in f])
        diff_arp=set(arp_entry).difference(s)

    diff_arp.discard("\n")
    
    #Update the arp_diff file for logging
    with open(arp_table_diff,'a+') as f_diff:
        for line in diff_arp:
            f_diff.write(f"{datetime.datetime.now()} : {line}\n")

    #Update the arp_table file with the new entries from the device
    with open(arp_table,'w') as f:
        for i in arp_entry:
            f.write("%s\n" % i)
    

    arp_content = ""
    for line in diff_arp:
        arp_content+=f"{datetime.datetime.now()} : {line}\n"

    msg_content = f"""
This is a test email to track arp_table changes:
{arp_content}
"""


    msg = EmailMessage()
    msg['Subject'] = 'Test Email' # Subject of Email
    msg['From'] = email_username
    msg['To'] = # Reciver of the Mail
    msg.set_content(msg_content) # Email body or Content

    #Code from here will send the message
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login(email_username,email_password) 
        smtp.send_message(msg) 
    
else:
    with open(arp_table,'w') as f:
        for i in arp_entry:
            f.write("%s\n" % i)




