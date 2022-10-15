from bs4 import *
import requests
import re
import os
import urllib.request

def folder_create(images, url):
    folder_name = input("Enter name of folder: ")
    os.mkdir(folder_name)
    download_images(images, url, folder_name)

def download_images(images,url, folder_name): #, folder_name):
    count = 0
    print(f"Found {len(images)} images")
    if len(images) != 0:
        for i, image in enumerate(images):
            image_link = url + "/" + image
            r = requests.get(image_link).content
            with open(f"{folder_name}/{image}", "wb+") as f:
                f.write(r)
                count+=1
        if count == len(images):
            print("All the images have been downloaded!")
        else:
            print(f" {count} images have been downloaded out of {len(images)}")


def main(url):
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

url = input("Enter site URL:")
main(url)
# import os 
# import inspect 
# print(os.path.dirname(inspect.getfile(inspect))+"/site-packages")