""" SendDragonBoardData.py
   Copyright 2016 OSIsoft, LLC.
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

#!/usr/bin/python
from __future__ import print_function
import os
import time
import json
import requests

#Wait 2min on startup to ensure Arduino sketch has started
time.sleep(120)

#Enter your UFL REST endpoint URL here:
url = 'https://{myuflserver}:5460/connectordata/{myuflendpoint}'

s = requests.session()
# In the Session information, one needs to set the username and password
# as specified in the connector configuration page
# You can hard code the credentials in the variables below.
# If not, you will be prompted to enter them at run time.
# If anonymous authentification is used, then use can use emptry strings for both
_username = None
_password = None

def username():
    global _username
    if _username is None:
        _username = getpass.getpass('Username: ')
    return _username
   
def password():
    global _password
    if _password is None:
        _password = getpass.getpass()
    return _password

s.auth = (username(), password())

#Disable warnings due to lack of server cert
requests.packages.urllib3.disable_warnings()

#Read file list from local json directory on OpenWRT
path = '/json/'

#while loop begin
try:
    while True:
        #Get current file list, sort, count files
        dirList=os.listdir(path)
        dirList.sort()
        fileCount = len(dirList)
        loopCount = 0
        print(fileCount - 1, " files in queue to process.")
        
        #Iterate through each file and post the file contents (JSON) to UFL REST endpoint
        for infile in dirList:
            #Iterate the counter first to ensure we leave at least one file in the directory
            loopCount += 1
            #If we've processed all but one file, exit the loop
            if loopCount == fileCount:
                break
                               
            #Open file and read contents, then close
            print("File being processed is: " + infile)
            f=open(os.path.join(path, infile),'r')
            payload=f.read()
            f.close()
        
            #Send file json content to UFL endpoint
            try:
                response = s.put(url, data=data, verify=False)
                # To use the Post method instead, replace the line above with the one below.
                # response = s.post(args.resturl + '/post', data=data, verify=False)
            except:
                #If we throw an exception, break and try again on the next loop
                print("Error during HTTP POST. Aborting loop.")
                break
            #If successful, delete the file
            if response.status_code == 200:
                os.remove(os.path.join(path, infile))
                print("Success. File " + infile + " was uploaded and deleted.")
            #else:
                print(response.status_code, response.reason, file=sys.stderr)
                print(" File " + infile + "was NOT uploaded and NOT deleted.")

        #Delay 10 seconds before next loop
        print("Waiting 10 seconds to run again.")
        time.sleep(10)
except KeyboardInterrupt:
    pass
