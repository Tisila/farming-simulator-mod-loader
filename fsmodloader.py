import os
import sys
import requests
from bs4 import BeautifulSoup

#File to read mod links from
links_file = 'fsmods.txt'

#Help for this in here https://www.geeksforgeeks.org/downloading-files-web-using-python/
def get_mod(source, filename, headers, size):
    wsize = 0
    response = requests.get(source, stream = True, headers = headers)
    with open(filename, 'wb') as zipfile:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                wsize += zipfile.write(chunk)
                wsize_MB = wsize/1024/1024
                sys.stdout.write('Downloaded {:.2f}/{:.2f} MB in file {}\r'.format(wsize_MB, size, 'filename'))
                sys.stdout.flush()
    print('Downloaded {:.2f}/{:.2f} MB in file {}\n'.format(wsize_MB, size, 'filename'))  

#Check if file doesn't exist
if not os.path.isfile(links_file):
    print('The file {} does not exist is the current directory\nPlease rename your file.'.format(links_file))
else:
    print('Found mods file, parsing mods list')
    #Reading lines and cleaning them
    with open(links_file) as f:
        links = f.readlines()
    links = [x.strip() for x in links]

    print('{} mods to download\n'.format(len(links)))

    #Downloading each mod
    for link in links:
        download_headers = {
            'Host': 'cdn30.giants-software.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': link,
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'}
        #Retrieving the mod landing page for mod download cdn link 
        r = requests.get(link)
        soup = BeautifulSoup(r.text, 'html.parser')
        html = list(soup.children)[2]
        body = list(html.children)[3]
        btn = body.find_all(class_='button-buy')[0]
        mod_link = btn['href']
        mod_name = mod_link.split('/')[-1]
        size_text = body.find_all(class_='table-cell')[9].get_text()
        size = float(size_text.split(' ')[0])
        #Downloading the mod
        print('Downloading {}'.format(mod_link))
        get_mod(mod_link, mod_name, download_headers, size)
    print('Download complete!')
