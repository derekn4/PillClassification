from bs4 import *
import requests
import re
import os
import urllib.request
from os.path import exists

def folder_create(images, url):
    folder_name = "images"
    download_images(images, url, folder_name)

def download_images(images,url, folder_name): #, folder_name):
    count = 0
    print(f"Found {len(images)} images")
    if len(images) != 0:
        for i, image in enumerate(images):
            image_link = url + "/" + image
            if not exists(f"{folder_name}/{image}"):
                r = requests.get(image_link).content
                with open(f"{folder_name}/{image}", "wb+") as f:
                    f.write(r)
                    count+=1
                
                #keeping track of image downloads
                if count%100 == 0:
                    print(f"{count} images downloaded from {url}")

        if count == len(images):
            print("All the images have been downloaded!")
        else:
            print(f" {count} images have been downloaded out of {len(images)}")


def main(urls):
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        links = []
        for link in soup.find_all("a"):
            #print(link)
            if link.get("href").endswith(".JPG"):
                #print(link.get("href"))
                links.append(link.get("href"))

        if url.endswith('/index.html'):
            url = url[:-11]
        #download_images(links, url)
        folder_create(links, url)

#url = input("Enter site URL:")
#main(url)

url = "https://data.lhncbc.nlm.nih.gov/public/Pills/index.html"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
links = []
for link in soup.find_all("a"):
    if link.get("href").startswith("PillProjectDisc"):
        links.append(link.get("href"))

curr = [l.strip('/index.html') for l in links[:5]]
for c in curr:
    print(c)

for l in range(len(links)):
    if links[l].endswith('/index.html'):
        links[l] = links[l][:-11]
        links[l] = "https://data.lhncbc.nlm.nih.gov/public/Pills/" + links[l] + "/images/index.html"

# for l in links:
#     print(l)
#folder_name = "images"
#os.mkdir(folder_name)
#print(links[:5])
#print(links[2:5])
main(links[3:5])