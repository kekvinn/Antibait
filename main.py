import cv2 as cv
import urllib.request
import numpy as np
from urllib.parse import urlparse, parse_qs
import pafy


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
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in {'www.youtube.com', 'youtube.com'}:
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/watch/':
            return query.path.split('/')[1]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]


# Acquires the thumbnail from the video
def fetch_thumbnail(url):
    req = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    thumbnail = cv.imdecode(arr, -1)

    return thumbnail


# Compares frames of video and the thumbnail
def compare(thumbnail, video):
    highest = 0
    while True:

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
            print(highest)

    video.release()
    cv.destroyAllWindows()


process_url()
