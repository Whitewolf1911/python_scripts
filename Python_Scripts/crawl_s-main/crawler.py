#!/usr/bin/env python

import requests


def get_response(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass


target_url = "10.0.2.7/mutillidae"
with open("/usr/share/wordlists/fsocity.dic", "r") as wordlist_file:
    for line in wordlist_file:
        # .strip() method removes all whitespace characters like space or \n newline etc.
        word = line.strip()
        test_url = target_url + "/" + word
        response = get_response(test_url)
        if response.status_code == 200:
            print("[+] Discovered URL --> " + test_url)
