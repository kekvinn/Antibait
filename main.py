import cv2 as cv
import urllib.request
import numpy as np
from urllib.parse import urlparse, parse_qs
import pafy
from datetime import timedelta


# Processes YouTube URL
def process_url():
    link = input('Please enter the YouTube Link: ')

    # Stores the YouTube video
    v_pafy = pafy.new(link)
    play = v_pafy.getbest(preftype="mp4")
    capture = cv.VideoCapture(play.url)

    # Stores the thumbnail of the video
    image_url = 'https://img.youtube.com/vi/' + extract_video_id(link) + '/maxresdefault.jpg'
    thumbnail = fetch_thumbnail(image_url)

    compare(thumbnail, capture)


# Gets the video ID of the video
def extract_video_id(url):
    if url.startswith(('youtu', 'www')):
        url = 'http://' + url

    query = urlparse(url)

    if 'youtube' in query.hostname:
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        elif query.path.startswith(('/embed/', '/v/')):
            return query.path.split('/')[2]
    elif 'youtu.be' in query.hostname:
        return query.path[1:]
    else:
        raise ValueError


# Acquires the thumbnail from the video
def fetch_thumbnail(url):
    req = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    thumbnail = cv.imdecode(arr, -1)

    return thumbnail


# Compares frames of video and the thumbnail
def compare(thumbnail, video):
    highest = 0
    frame_at_highest = 0
    frame_count = int(video.get(cv.CAP_PROP_FRAME_COUNT))

    for i in range(frame_count):
        is_true, frame = video.read()
        vid_size = frame.shape
        (height, width, useless) = vid_size

        thumbnail = cv.resize(thumbnail, (width, height))

        if cv.waitKey(1) & 0xFF == ord('d'):
            break

        if thumbnail.shape == frame.shape:
            res = cv.absdiff(thumbnail, frame)
            res = res.astype(np.uint8)
            percentage = 100 - (np.count_nonzero(res) * 100) / res.size

        if percentage > highest:
            highest = percentage
            frame_at_highest = i

    convert_to_time(frame_at_highest)
    video.release()
    cv.destroyAllWindows()


def convert_to_time(frame_count):
    fps = 30.0
    td = timedelta(seconds=(frame_count / fps))
    print(td)


process_url()
