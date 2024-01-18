import tweepy
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.client import OAuth2Credentials
import requests
from io import BytesIO

# Tweepy authentication
bearer_token = os.environ.get("BEARER_TOKEN")
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
    wait_on_rate_limit=True,
)


# Google Drive authentication
gauth = GoogleAuth()
gauth.credentials = OAuth2Credentials(
    access_token=None,  
    client_id=os.environ.get("CLIENT_ID"),  
    client_secret=os.environ.get("CLIENT_SECRET"),  
    refresh_token=os.environ.get("REFRESH_TOKEN"),  
    token_expiry=None,
    token_uri='https://accounts.google.com/o/oauth2/token',  
    user_agent='pyDrive', 
    revoke_uri='https://accounts.google.com/o/oauth2/revoke'  
)
drive = GoogleDrive(gauth)

# Google drive folder id https://drive.google.com/drive/u/0/folders/1L0MJqJx-qirE9K1Sdy2W2SyYWNo_wY_Q
folder_id = '1L0MJqJx-qirE9K1Sdy2W2SyYWNo_wY_Q'  

file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()

# Sorting
file_list.sort(key=lambda x: x['title'])

# Read the index of the last tweeted photo from a file
with open('last_tweeted_photo_index.txt', 'r') as f:
    last_tweeted_photo_index = int(f.read().strip())

# index that need to be tweeted this time
photo_index = last_tweeted_photo_index + 1

# Getting image from Google Drive using BytesIO
file = file_list[photo_index]
response = requests.get(file['webContentLink'])
image_file = BytesIO(response.content)

# media_upload() will upload the image and return a media object
media = api.media_upload(filename=file['title'], file=image_file)

# Common caption for all tweets
caption = f"#DevaraGlimpse - Frame {photo_index} of {len(file_list)} Frames."

# Tweet with the image and caption
tweet = client.create_tweet(text=caption, media_ids=[media.media_id])

print(f"Tweeted image: {file['title']}")

# Updates the index of the last tweeted photo
with open('last_tweeted_photo_index.txt', 'w') as f:
    f.write(str(photo_index))

