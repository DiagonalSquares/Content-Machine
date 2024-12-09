import downloader
import edit
import os
import time

os.makedirs(os.getcwd() + "//clips", exist_ok=True)
os.makedirs(os.getcwd() + "//Finished Products", exist_ok=True)

while True:
    print("Starting the Scrape Process\n")
    downloader.scrape()
    twitch_clips = os.listdir(os.getcwd() + "\clips")
    for clip in twitch_clips:
        try:
            print("Starting editing process")
            edit.edit_video(os.getcwd() + "\clips\\" + clip, "finished_clip" + str(clip))
        except:
            print("An error occured while editing, good luck")
        try:
            if os.path.exists(os.getcwd() + "\clips\\" + clip):
                os.remove(os.getcwd() + "\clips\\" + clip)
        except:
            print("unable to remove one of the clips, time to cope and delete it manually")

        print("Session Complete///")

    time.sleep(86000)