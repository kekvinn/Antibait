from googleapiclient.discovery import build
import config

api_key = config.api_key

youtube = build('youtube', 'v3', developerKey=api_key)
