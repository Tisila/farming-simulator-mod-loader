import os
import sys
import requests
from bs4 import BeautifulSoup

#File to read mod links from
links_file = 'fsmods.txt'

class Mod:
    def __init__(self, webpage):
        """
        Defines a mod object with the webpage link to retrieve data.

        :param webpage: Website link as string
        """
        self._webpage = webpage
        self._link = ""
        self._size = 0
        self._unit = ""
        self._filename = ""
        self.get_information()

    def is_updated(self):
        return False

    def is_downloaded(self):
        return os.path.isfile(self._filename)

    def get_information(self):
        """
        Retrieves the object data from the webpage.
        """
        #Retrieving the mod landing page for mod download information
        r = requests.get(self._webpage)
        soup = BeautifulSoup(r.text, 'html.parser')
        html = list(soup.children)[2]
        body = list(html.children)[3]
        btn = body.find_all(class_='button-buy')[0]
        self._link = btn['href']
        self._filename = self._link.split('/')[-1]
        size_data = body.find_all(class_='table-cell')[9].get_text().split(' ')
        self._size = float(size_data[0])
        self._unit = size_data[1] 

    def download(self):
        """
        Downloads the mod zip through the object data.
        """
        #Defining headers
        download_headers = {
                'Host': 'cdn30.giants-software.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Referer': self._webpage,
                'Upgrade-Insecure-Requests': '1',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache'}
        #Download file
        #Help for this in here https://www.geeksforgeeks.org/downloading-files-web-using-python/
        wsize = 0
        response = requests.get(self._link, stream = True, headers = download_headers)
        with open(self._filename, 'wb') as zipfile:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    wsize += zipfile.write(chunk)
                    wsize_MB = wsize/1024/1024
                    m = 'Downloaded {:.2f}/{:.2f} MB in file {}\r'
                    sys.stdout.write(m.format(wsize_MB, self._size, 'filename'))
                    sys.stdout.flush()
        #Download complete
        m = 'Downloaded {:.2f}/{:.2f} MB in file {}\n'
        print(m.format(wsize_MB, self._size, 'filename'))  

if __name__=="__main__":
    #Check if file doesn't exist
    if not os.path.isfile(links_file):
        m = 'The file {} does not exist in the current directory\nPlease rename your file.'
        print(m.format(links_file))
    else:
        print('Found mods file, parsing mods list')
        #Reading lines and cleaning them
        with open(links_file) as f:
            links = f.readlines()
        links = [x.strip() for x in links]

        print('{} mods to download\n'.format(len(links)))

        #Downloading each mod
        mods = []
        for link in links:
            mods.append(Mod(link))

        #Downloading the mods
        for mod in mods:
            if not mod.updated:
                print('Downloading {}'.format(mod_link))
                mod.download(mod_link, mod_name, download_headers, size)
        print('Download complete!')
