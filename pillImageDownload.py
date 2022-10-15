from bs4 import *
import requests
import re
import os
import urllib.request

def folder_create(images):
    folder_name = input("Enter name of folder: ")
    os.mkdir(folder_name)
    download_images(images, folder_name)
def download_images(images,url): #, folder_name):
    count = 0
    print(f"Found {len(images)} images")
    if len(images) != 0:
        for i, image in enumerate(images):
            print(i, image)
            image_url = url + "/" + image, "wb+"
            r = requests.get(url).content
            print(image_url)
            print(r)
            break
            # with open(image_url + "/" + image, "wb+") as f:
            #     response = requests.get()
            #image_link = image["src"]
            #r = requests.get(image).content
            #print(image)
        #     with open(f"{r}", "wb+") as f:
        #         f.write(r)
        #         count += 1
        # if count == len(images):
        #     print("All the images have been downloaded!")
        # else:
        #     print(f" {count} images have been downloaded out of {len(images)}")


def main(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    #print(soup)
    #images = soup.findAll('.JPG')
    #print(images)
    #folder_create(images)
    #links = soup.findAll("a", href= re.compile("\.txt$"))
    print(soup.find_all("a"))
    links = []
    for link in soup.find_all("a"):
        #print(link)
        if link.get("href").endswith(".JPG"):
            print(link.get("href"))
            links.append(link.get("href"))

    if url.endswith('/index.html'):
        url = url[:-11]
    download_images(links, url)

url = input("Enter site URL:")
main(url)