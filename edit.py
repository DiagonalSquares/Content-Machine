import os
from pathlib import Path
from moviepy.editor import VideoFileClip, CompositeVideoClip # type: ignore
from moviepy.editor import ColorClip # type: ignore
from moviepy.video.fx import all as vfx # type: ignore
import cv2 # type: ignore
import random

VIDEO_NAME = "" #put your own video name here

def blur_frame(frame):
    if frame is None or frame.size == 0:
        return frame
    return cv2.GaussianBlur(frame, (51, 51), 0)

def edit_video(raw_clip, name):
    clip = VideoFileClip(raw_clip)
    #shorts format: 1080x1920
    clip = clip.resize((1080, 608))

    black_clip = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=clip.duration)

    duration = clip.duration

    if duration >= 30:
        other_black_clip = ColorClip(size=(1080, 1216), color=(0, 0, 0), duration=clip.duration)

        parjour = VideoFileClip(os.getcwd() + f"\{VIDEO_NAME}" )
        parjour_duration = int(parjour.duration)

        random_start = random.randrange(0, parjour_duration)
        end = random_start + duration

        if end >= parjour_duration:
            random_start -= 60
            end -= 60

        parjour = parjour.subclip(random_start, end)
        parjour = parjour.resize((1080, 608))

        parjour = parjour.set_position(('bottom'))

        new_clip = CompositeVideoClip([other_black_clip, parjour, clip])

        new_clip = new_clip.set_position('center')
    else:
        new_clip = clip

        new_clip = new_clip.set_position('center')
    
    blurred_clip = new_clip.resize((3340, 1920))
    blurred_clip = blurred_clip.fl_image(blur_frame)

    blurred_clip = blurred_clip.crop(x1=((3340-1080)/2), x2=(blurred_clip.w-(3340-1080)/2))

    finished_clip = CompositeVideoClip([blurred_clip, new_clip])

    os.chdir(os.getcwd() + "\Finished Clips")
    finished_clip.write_videofile(name, fps=60)
    os.chdir(Path(os.getcwd()).parent)
    

    print("Succesfully finished editing this Video///")