import os
from selenium import webdriver # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.common.by import By # type: ignore
import yt_dlp # type: ignore
import json

with open(os.getcwd() + "\\clips_done.json") as f:
    clips_done = json.load(f)
    f.close()

#scrapes info about Twitch Clips from Twitchtracker and parses it using BeautifulSoup; Filters out any clips with less than 100k views
def scrape():
    url = "https://twitchtracker.com/clips"

    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    driver.get(url)

    clip_class = driver.find_elements(By.CLASS_NAME, "clip-tp")
    clip_views = driver.find_elements(By.CLASS_NAME, "clip-views")
    clip_titles = driver.find_elements(By.CLASS_NAME, "clip-title")
    
    print("successfully found all clip urls, names, and view counts")

    clip_views_cleaned = []
    for item in clip_views:
        cleaned = item.text.replace(",", "")
        cleaned = int(cleaned.replace("views", ""))
        clip_views_cleaned.append(cleaned)

    twitch_urls = []
    clip_names = []
    for item in range(len(clip_views_cleaned)):
        if clip_views_cleaned[item] >= 100000:
            twitch_urls.append("https:" + clip_class[item].get_attribute("data-litebox"))
            name = clip_titles[item].get_attribute("title")
            clip_names.append(name)
    
    driver.quit()
    
    print("\nstarting download process")

    for item in range(len(twitch_urls)):
        download(twitch_urls[item], clip_names[item])
        #time.sleep(1)

#Downloads Twitch Clips if the video has not been made into short form content yet
def download(url, name):
    service = Service(executable_path=r"C:\Users\ianbi\Desktop\Projects\ContentMachine\Content Machine\chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    driver.get(url)

    video = driver.find_element(By.TAG_NAME, "video")

    clip_url = video.get_attribute("src")
        
    driver.quit()

    clip = str(clip_url)

    print("checking if clip download shall proceed")

    has_clip = False
    for item in clips_done['videos']:
        if name == item:
            has_clip = True

    if has_clip == False:
        print("did not have this clip, very cool")

        clips_done['videos'].append(name)

        with open(os.getcwd() + "\\clips_done.json", "w") as f:
            json.dump(clips_done, f)
            f.close()

        save_directory = os.getcwd() + "//clips"

        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(save_directory, name + '.%(ext)s'),
        }

        print("Beginning Download")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([clip])
            except:
                print("there was an error downloading this clip, womp womp i guess idk")

    else:
        print("already have this clip")
        print("Skipping Download")
    
    print("Downloading complete///")