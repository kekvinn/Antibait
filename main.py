import cv2 as cv
import urllib.request
import numpy as np
from urllib.parse import urlparse, parse_qs
import pafy


# Processes YouTube URL
def process_url():
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


# Converts a frame into a timestamp
def convert_to_time(frame_count):
    fps = 30.0
    seconds = round(frame_count / fps)
    minutes = 0
    hours = 0

    while seconds > 60:
        seconds -= 60
        minutes = minutes + 1

    while minutes > 60:
        minutes -= 60
        hours = hours + 1

    if seconds < 10:
        seconds = '0' + str(seconds)

    if hours > 0:
        if minutes < 10:
            minutes = '0' + str(minutes)
        timestamp = str(hours) + ':' + str(minutes) + ':' + str(seconds)
    else:
        timestamp = str(minutes) + ':' + str(seconds)

    print(timestamp)
    make_new_link(seconds)


# Creates a new link that leads to where the thumbnail appears in the video
def make_new_link(seconds):
    new_link = 'https://youtu.be/' + extract_video_id(link) + '?t=' + str(seconds)
    print('Link: ' + new_link)


if __name__ == '__main__':
    link = input('Please enter the YouTube Link: ')
    process_url()

