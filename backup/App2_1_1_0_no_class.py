# youtube downloader
import os
import eel
from collections import namedtuple
from pytube.extract import mime_type_codec
from youtubesearchpython import SearchVideos
from colorama import *
import Temprorary as Temp
from History import History
from pytube import YouTube
from Filename import *
import subprocess
import time
import json
import requests

# operation system color initialized
os.system("")

# --- declare global static  variable --- #
ds = ""
video = ""  # YouTube(url, on_progress_callback=True)
result = "" # video.streams
history = {}
file_size = 0
path = ""
# --------------------------------------- #

@eel.expose
def refresh():
    global path
    global ds
    ds = ""
    path = ""
    print(f"{Fore.GREEN}(Listening){Fore.RESET} to {Fore.BLUE}Python{Fore.RESET}")

# --- datasource configuration --- #
def search(_title, _offset, _mode, _count):
    return SearchVideos(
        _title,
        offset=_offset,
        mode=_mode,
        max_results=_count
    )
# -------------------------------- #

# --- init data --- #
def fetch_search(ctx):
    ctx = ctx.result()
    data = json.loads(ctx)
    for _data in data["search_result"]:
        _title = _data["title"]
        print("[x]", _title)
    return data
# ----------------- #

# --- make object --- #
def get_result(source):
    data = source["search_result"]
    eel.clearObj()
    for idx in data:
        _id = idx["id"]
        _title = idx["title"]
        _channel = idx["channel"]
        _viewer = idx["views"]
        _imgurl = idx["thumbnails"][4]
        _link = idx["link"]
        eel.makeObj(_id, _title, _channel, _viewer, _imgurl, _link)
# ------------------- #

# --- get datasource videos --- #
def init_search(title):
    global ds
    ds = fetch_search(
        search(
            title,
            1,
            "json",
            15
        )
    )
    get_result(ds)
# ----------------------------- #

@eel.expose
def search_videos(title):
    init_search(title)

# --- number checker whether positive or negative --- #
def number_is_positive(number):
    if number >= 0:
        return True
    else:
        return False
# --------------------------------------------------- #

# --- get progress (core) download --- #
def on_progress(chunk, file_handler, bytes_remaining):
    global file_size
    size = file_size

    # --- get progress value (float) --- #
    progress = (100 * (size - bytes_remaining)) / size
    # ---------------------------------- #

    # --- checking whether progress not negative value --- #
    if number_is_positive(progress) & int(progress) <= 100:
        print(f"{int(progress)}% Downloading...")
    # ---------------------------------------------------- #

    # --- checking whether value is 100 (completed) --- #
    if int(progress) == 100:
        print(f"{int(progress)}% Download Completed!")
    # ------------------------------------------------- #
# ------------------------------------ #

# -- set video information --- #
@eel.expose
def Video(url, row_idx):
    global video
    global result
    print("Initializing, please wait...")
    video = YouTube(url, on_progress_callback=on_progress)
    result = video.streams
    print("Initializing done.")
    for data in quality():
        if data != False:
            print(data)
            eel.object_resolution(row_idx, data.resolution, data.itag)
# ---------------------------- #

# --- get info video.streams --- #
def str_getInfo(streams):
    ([(print(i, sep="\n")) for i in streams])
# ------------------------------ #

# --- get the best audio quality object (160kbps) audio/webm opus --- #
def get_audio(streams):
    global file_size
    # --- priority get (160kbps) opus audio/webm --- #
    audio1 = [i for i in streams.filter(
        adaptive=True,
        mime_type="audio/webm"
    )]
    # ---------------------------------------------- #

    # --- [BUG] --- #
    # --- second priority get (128kbps) mp4 audio/mp4 --- #
    audio2 = streams.get_audio_only()
    # --------------------------------------------------- #

    # --- absolute return only 1 file --- #
    if len(audio1) == 1:
        file_size = 0
        file_size = audio1[0].filesize
        return audio1[0]
    # ----------------------------------- #
    # --- another (X-160)kbps initialized --- #
    elif len(audio1) > 1:
        audio1 = streams.filter(
            adaptive=True,
            mime_type="audio/webm",
            abr="160kbps"
        )
        # --- priority 160kbps --- #
        if len(audio1) > 0:
            file_size = 0
            file_size = audio1[0].filesize
            return audio1[0]
        # ------------------------ #
    # --- [BUG] --- #
    # --- getting 128kbps audio --- #
    else:
        file_size = 0
        file_size = audio2.filesize
        return audio2
    # ----------------------------- #
# ------------------------------------------------------------------- #

# --- get downloadable video based on filter quality --- #
def get_downloadable(streams):
    # --- set prototype property callable --- #
    prototype = namedtuple("get_downloadable", ["res480", "res720", "res1080", "res1440", "res2160"])
    # ------------------------------------- #

    # --- list of video each quality filtered [480-2160] --- #
    _480p = [i for i in streams.filter(
        adaptive=True,
        resolution="480p",
        mime_type="video/mp4"
    )]
    _720p = [i for i in streams.filter(
        adaptive=True,
        resolution="720p",
        mime_type="video/mp4"
    )]
    _1080p = [i for i in streams.filter(
        adaptive=True,
        resolution="1080p",
        mime_type="video/mp4"
    )]
    _1440p = [i for i in streams.filter(
        adaptive=True,
        resolution="1440p"
    )]
    _2160p = [i for i in streams.filter(
        adaptive=True,
        resolution="2160p"
    )]
    # ----------------------------------------------------- #
    return prototype(_480p, _720p, _1080p, _1440p, _2160p)
# --------------------------------------------------------- #

# --- returning best fps (60) if available, default is (30) --- #
def fps_cleansing(source):
    # --- set cleansing property callable --- #
    cleansing = namedtuple("cleansing", ["res480", "res720", "res1080", "res1440", "res2160"])
    # --------------------------------------- #

    # --- set cleansing property each res from get_downloadable() --- #
    cleansing_480 = get_downloadable(source).res480
    cleansing_720 = get_downloadable(source).res720
    cleansing_1080 = get_downloadable(source).res1080
    cleansing_1440 = get_downloadable(source).res1440
    cleansing_2160 = get_downloadable(source).res2160
    # --------------------------------------------------------------- #
    
    # --- cleansing fps, force to get (60) if available, keep 30 if not available --- #
    def clean(cleansing):
        if len(cleansing) > 1:
            for i in cleansing:
                if i.fps == 60:
                    pass
                else:
                    if len(cleansing) > 1:
                        cleansing.remove(i)
                    else:
                        pass
        if len(cleansing) == 1:
            return cleansing[0]
        else:
            return False
    # ------------------------------------------------------------------------------- #

    # --- based on get_downloadable (output), checking if the're available for (60) than 30 --- #
    cleansing_480 = clean(cleansing_480)
    cleansing_720 = clean(cleansing_720)
    cleansing_1080 = clean(cleansing_1080)
    cleansing_1440 = clean(cleansing_1440)
    cleansing_2160 = clean(cleansing_2160)
    # ----------------------------------------------------------------------------------------- #

    # --------------------------------------------------------- #
    return cleansing(cleansing_480, cleansing_720, cleansing_1080, cleansing_1440, cleansing_2160)
# ------------------------------------------------------------- #

# --- merging file after completed the download file(s) --- #
def merge(pathfile_video, pathfile_audio):
    # --- (output) path save directory --- #
    path_save = "D:\yanagihara\python\downloader"
    # ------------------------------------ #

    # --- (output) filename --- #
    output_name = f"{cleansing(video.title)}.mp4"
    # ------------------------- #

    # --- [FIX IT] -> Just used double quote instead double backslash --- #
    # --- replacing backslash into single reverse one --- #
    pathfile_video = pathfile_video.replace("\\", "/")
    pathfile_audio = pathfile_audio.replace("\\", "/")
    # --------------------------------------------------- #

    # --- Merge command ffmpeg pre-processing video audio --- #
    command_merge = f'ffmpeg.exe -i "{pathfile_video}" -i "{pathfile_audio}" -c copy -c:a aac "{os.path.join(path_save, output_name)}"'
    # ------------------------------------------------------- #

    # --- Execute command merge based ffmpeg.exe --- #
    run_command(command_merge)
    # ---------------------------------------------- #
    return "Merging file(s) completed."
# --------------------------------------------------------- #

# --- execute command under subprocess.call module --- #
def run_command(command):
    try:
        # --- get time process begin --- #
        start = time.time()
        # --------------------------------- #
        print("Please wait, merging process being run...")

        # --- execute command shell based {command} --- #
        subprocess.call(
            command,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        # --------------------------------------------- #

        # --- get time after process --- #
        end = time.time()
        # ------------------------------ #

        # --- calculate elapsed time process --- #
        print("Merge and rewrite done. Elapsed : %.2fsec." % (end-start))
        # -------------------------------------- #
    
    # --- raise Exception error --- #
    except Exception as ex:
        print(ex)
    # -------------------------------- #
# ---------------------------------------------------- #

# --- add filename, pathvideo, pathaudio to dictionary --- #
def add_to_history(path):
    global video
    global history

    # --- joining path and title with static extension --- #
    video_path = os.path.join(path, cleansing(video.title) + ".mp4")
    audio_path = os.path.join(path, cleansing(video.title) + ".webm")
    # ---------------------------------------------------- #

    # --- merging video audio and fixing video codec by ffmpeg --- #
    merge(video_path, audio_path)
    # ------------------------------------------------------------ #

    # --- declare dummy History object --- #
    _history = History(video.title, video_path, audio_path)
    # ------------------------------------ #

    # --- assignment history to global history based dictionary datatype --- #
    history[_history.getKey] = _history.getValue
    # ---------------------------------------------------------------------- #
# -------------------------------------------------------- #

# --- cleaning temprorary video audio --- #
def delete_after_download():
    try:
        # --- global initialized --- #
        global history
        global video
        # -------------------------- #

        print("Prepare for cleaning temprorary file(s).")

        # --- adding delay on running the code --- #
        time.sleep(3.5)
        # ---------------------------------------- #

        # --- fetching video path, audio path from history dictionary --- #
        datapath = [history[cleansing(video.title)][x] for x in history[cleansing(video.title)]]
        # --------------------------------------------------------------- #

        # --- removing datafile(s) if exist. (default=True) --- #
        for path in datapath:
            if os.path.isfile(path):
                os.remove(path)
        # ----------------------------------------------------- #
    
    # --- raise Exception error --- #
    except Exception as ex:
        print(ex)
    # ----------------------------- #
# --------------------------------------- #

# --- (semi-core) fetching video quality and prototype --- #
@eel.expose
def quality():
    global result
    source = fps_cleansing(result)
    print(source)
    return source
# -------------------------------------------------------- #

# --- (core) download video-audio based result.streams and quality prototype --- #
@eel.expose
def core_download(source, quality):
    try:
        # --- global initialized --- #
        global history
        global file_size
        # -------------------------- #
        file_size = 0

        # --- get path-temp on system based from Temprorary module --- #
        path = Temp.system_gettemp()
        # ------------------------------------------------------------ #

        # --- default is object. bool is False / resolution not identified --- #
        # --- regardless resolution is initialized when tried to download --- #
        if type(quality) != bool:
            print("Please wait until downloading finished...")

            # --- webm opus (160)kbps is priority --- #
            # --- get best audio to download --- #
            get_audio(source).download(path)
            # ---------------------------------- #

            # --- determine file size --- #
            file_size = quality.filesize
            # --------------------------- #

            # (semi-core as core) with quality based to download (2nd) --- #
            quality.download(path)
            # ------------------------------------------------------------ #
            
            # --- core backend process --- #
            # --- adding datainfo to history dictionary --- #
            add_to_history(path)
            # --------------------------------------------- #
            # --- immediately delete the temprorary file(s) after all downloaded --- #
            delete_after_download()
            # ---------------------------------------------------------------------- #
            
            print("Download completed.")
        
        # --- regardless resolution is not initialized when tried to download --- #
        else:
            print("can't download. not exist!")

    # --- raise Exception error --- #
    except Exception as ex:
        print(ex)
    # ----------------------------- #
# ------------------------------------------------------------------------------ #


# --- eel --- #

eel.init("www")
eel.start("App2.html")