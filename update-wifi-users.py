#!/usr/bin/env python3

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import hashlib
import subprocess

# google api credentials for google drive API
scope = ['https://spreadsheets.google.com/feeds']
cred_file = '/home/aecc-directiva/wifi_manage/aecc-uprrp-google-api.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Formulario para Ingresar a AECC (Responses)").sheet1

# acquire student numbers
sids = sheet.col_values(6)

# acquire phone numbers
phones = sheet.col_values(7)

# bool confirming members have payed
confirmation = sheet.col_values(19)

# freeradius users entries
entries = []

# parse all entries and only add them if it's a confirmed member
for i in range(1,len(sids)):
	if (confirmation[i] == '1'):
		user = sids[i]
		pswd = "AECC-" + phones[i][-4::]
		entry = "{} Cleartext-password :=\"{}\"".format(user, pswd)
		#print(entry)
		entries.append(entry)

template = '/etc/freeradius/users.template'
users = '/etc/freeradius/users'

with open(template, 'r') as f: content = f.readlines()
with open(users, 'r') as u: curr = u.read()

for e in entries:
	content.append(e+"\n")
c = ''.join(content)

f.close()

# calculate md5 sums of current users file and potential new one
curr_hash = hashlib.md5(curr.encode('utf-8')).hexdigest()
c_hash = hashlib.md5(c.encode('utf-8')).hexdigest()

u.close()

# if our created new file is different from our current one,
# then overwrite the old one and restart the freeradius service
if(c_hash != curr_hash):
    with open(users, 'w') as f: f.write(c)
    f.close()
    subprocess.run(['service', 'freeradius', 'restart'])
