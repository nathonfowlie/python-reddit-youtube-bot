from moviepy.editor import *  
import random 
from pathlib import Path
import textwrap
import nltk
from nltk.corpus import stopwords
import random
import logging 


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ])

def random_hex_colour():
    r = lambda: random.randint(0,255)
    rcolor = '#%02X%02X%02X' % (r(),r(),r())
    print("Generated random hex colour") 
    print(rcolor)
    return rcolor

def random_rgb_colour():
    rbg_colour = random.choices(range(256), k=3)
    print("Generated random rgb colour") 
    print(rbg_colour)
    return rbg_colour

def get_font_size(length):

    fontsize = 50
    lineheight = 60

    if length < 10 :
        fontsize = 190
        lineheight = 200

    if length >= 10 and length < 20:
        fontsize = 180
        lineheight = 190

    if length >= 20 and length < 30:
        fontsize = 170
        lineheight = 180

    if length >= 30 and length < 40:
        fontsize = 130
        lineheight = 150

    if length >= 40 and length < 50:
        fontsize = 130
        lineheight = 120

    if length >= 50 and length < 60:
        fontsize = 140
        lineheight = 140

    if length >= 60 and length < 70:
        fontsize = 120
        lineheight = 120

    if length >= 70 and length < 80:
        fontsize = 115
        lineheight = 110

    if length >= 80 and length < 90:
        fontsize = 115
        lineheight = 110

    if length >= 90 and length < 100:
        fontsize = 80
        lineheight = 100

    logging.info(f"Title Length       : {length}")
    logging.info(f"Setting Fontsize   : {fontsize} " )
    logging.info(f"Setting Lineheight : {lineheight} " )

    return fontsize, lineheight


def generate(video, filepath):
    logging.info('========== Generating Thumbnail ==========')

    colors = ["#FFA500","#B8FF72","#FFC0CB","#89cff0","#ADD8E6","green","yellow","red"]
    stop_word_colour = random.choice(colors)

    image = random.choice(os.listdir("images"))
    image_path = str(Path("images", image))
    logging.info('Randomly Selecting Background : ' + image_path)
    text = video.meta.title
    subreddit = video.meta.subreddit_name_prefixed
    nltk.download('stopwords')
    s=set(stopwords.words('english'))
    words = text.split(" ")
    unique_words = list(filter(lambda w: not w in s,text.split()))

    clips = []

    margin = 40
    txt_y = 0 + margin
    txt_x = 0 + margin
    width = 1280
    height = 720
    #fontsize = get_font_size(len(video.meta.title))
    fontsize, lineheight = get_font_size(len(video.meta.title))


    background_clip = TextClip("",
                            size=(width,height), 
                            bg_color="#000000",
                            method="caption").margin(20, color=random_rgb_colour())

    clips.append(background_clip)

    img_width = width/2
    img_clip = ImageClip(image_path).resize(width=img_width, height=height)\
                                    .set_position(("right","bottom"))\
                                    .set_opacity(0.8)

    clips.append(img_clip)

    subreddit_clip = TextClip(subreddit,
                        fontsize = 80, 
                        color="white", 
                        align='center', 
                        font="Verdana-Bold", 
                        bg_color="#000000",
                        method="caption")\
                        .set_pos((margin, 20))\
                        #.set_opacity(0.8)

    clips.append(subreddit_clip)

    txt_y += subreddit_clip.h

    for word in words:
        if word in unique_words:
            word_color = "white"
        else:
            word_color = stop_word_colour

        if txt_x > (width / 2):
            txt_x = 0 + margin
            txt_y += lineheight

        txt_clip = TextClip(word,
                            fontsize = fontsize, 
                            color=word_color, 
                            align='center', 
                            font="Impact", 
                            #bg_color="#000000",
                            method="caption")\
                            .set_pos((txt_x, txt_y))
                            #.set_opacity(0.8)

        clips.append(txt_clip)
        txt_x += txt_clip.w + 15
        

    txt_clip = txt_clip.set_duration(10)
    txt_clip = txt_clip.set_position(("center","center"))


    final_video = CompositeVideoClip(clips)
    logging.info('Save Thumbnail to : ' + filepath)
    final_video.save_frame(filepath, 1)

if __name__ == "__main__":
    class meta():
        title = "What is the correct answer to ‘would you still love me if I was a worm' fhdngh apple"
        subreddit_name_prefixed = "r/askreddit"

    class Video():
        meta=None

    meta = meta()
    video = Video()
    video.meta = meta

    generate(video, "thumbnail.png")