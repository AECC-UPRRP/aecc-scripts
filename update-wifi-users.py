#!/usr/bin/env python3

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# google api credentials for google drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/aecc-directiva/wifi_manage/aecc-uprrp-google-api.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Formulario para Ingresar a AECC (Responses)").sheet1

# Extract and print all of the values
#list_of_hashes = sheet.get_all_records()
table = sheet.get_all_values()


sids = sheet.col_values(6)

phones = sheet.col_values(7)

confirmation = sheet.col_values(19)

entries = []

for i in range(1,len(sids)):
	if (confirmation[i] == '1'):
		user = sids[i]
		pswd = "AECC-" + phones[i][-4::]
		entry = "{} Cleartext-password :=\"{}\"".format(user, pswd)
		#print(entry)
		entries.append(entry)
with open('/etc/freeradius/users.template', 'r') as f: content = f.readlines()
#print(content)

for e in entries:
	content.append(e+"\n")
c = ''.join(content)
#print(c)
with open('/etc/freeradius/users', 'w') as f: f.write(c)
