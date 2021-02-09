# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 13:48:23 2020

@author: bazif
"""

import praw
import Downloader
import os
from tqdm import tqdm
import threading 
import time
reddit = praw.Reddit(
     client_id="MenNTxyAC0M9DA",
     client_secret="jqkxNYI0qEb0UlUw4Nk7E-oP-UjaDQ",
     user_agent="RedditImageScraper.v2"
 )

links = []
num_threads = 0
subreddit = "wallpapers"
import PySimpleGUI as sg
 
layout = [[sg.Text("Enter name of Subreddit")],
           [sg.Input(key="subreddit")],
           [sg.Text("Enter Number Of Threads")],
           [sg.Input(key="num_threads")],
           [sg.Button("Enter")],
           ]

window = sg.Window("Reddit Image Scraper",layout)

while True :
    event,values = window.read()
    
    if event == sg.WINDOW_CLOSED or event == "Enter":
        num_threads = int(values["num_threads"])
        subreddit = values["subreddit"]
        break
window.close()

for submission in (tqdm(reddit.subreddit(subreddit).hot(limit=None))):
    links.append(submission.url)


d = Downloader.Downloader(links,num_threads)
d.create_dir(subreddit,os.getcwd())

def initiate_download():
    d.start_downloading()




d_thread = threading.Thread(target=initiate_download)
d_thread.start()

layout = [[sg.Text('Downloading')],
          [sg.ProgressBar(101, orientation='h', size=(20, 20), key='progbar')],
          [sg.Cancel()]]

window = sg.Window('Download in Progress', layout)
while(d_thread.is_alive()):
    event, values = window.read(timeout=0) 
    prog=int(d.progress/len(links)*100)
    time.sleep(1)
    window["progbar"].update_bar(prog)

d_thread.join()
window.close()
