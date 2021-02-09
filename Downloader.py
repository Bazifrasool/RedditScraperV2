# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 13:48:23 2020

@author: bazif
"""
from concurrent.futures import ThreadPoolExecutor
import threading
import os
import requests
import uuid
import sys
import shutil
class Downloader:
    
    def __init__(self,list_of_links,workers = 100):
        self.list_of_links = list_of_links
        self.n_workers = workers
        self.progress = 0
    def download(self,link):
       response = requests.get(link)
       file = open(uuid.uuid4().hex+link[-5:], "wb")
       file.write(response.content)
       file.close()
       self.progress = self.progress+1
    def create_dir(self,name,path):
       os.chdir(path)
       try:
           os.mkdir(name)
           os.chdir(name)
       except:
           try:
               shutil.rmtree(name)
               os.mkdir(name)
               os.chdir(name)
           except:
               print("folder already exists, please delete older folder")
               sys.exit()
       
    def start_downloading(self):
         with ThreadPoolExecutor(max_workers=self.n_workers) as executor:
             executor.map(self.download, self.list_of_links)