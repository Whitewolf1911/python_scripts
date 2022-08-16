#!/usr/bin/env python
import requests
import re
import urllib.parse as urlparse

# use THIS SCRIPT WITH PYTHON3 !

target_url = "http://10.0.2.7/mutillidae/"
target_links = []


def extract_links_from(url):
    response = requests.get(url)
    return re.findall('(?:href=")(.*?)"', str(response.content))
    # you can do response.content.decode(errors="ignore") instead of this ^^^

def crawl(url):
    href_links = extract_links_from(url)
    # response.content shows us raw html code of the website
    for link in href_links:
        link = urlparse.urljoin(url, link)

        if "#" in link:
            link = link.split("#")[0]
            # this line is for printing the unique

        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)
            # making the function recursive


crawl(target_url)
