import tweepy
import os
import random
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.client import OAuth2Credentials
import requests
from io import BytesIO

# Authenticate using environment variables
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
    access_token=None,  # set access_token to None
    client_id=os.environ.get("CLIENT_ID"),  # these values are obtained from the "cloud console"
    client_secret=os.environ.get("CLIENT_SECRET"),  # these values are obtained from the "cloud console"
    refresh_token=os.environ.get("REFRESH_TOKEN"),  # obtained by running the auth flow on a local machine
    token_expiry=None,
    token_uri='https://accounts.google.com/o/oauth2/token',  # Google's token URI
    user_agent='pyDrive',  # you can set this to any string
    revoke_uri='https://accounts.google.com/o/oauth2/revoke'  # Google's revoke URI
)
drive = GoogleDrive(gauth)

# Specify the Google Drive folder ID
folder_id = '1L0MJqJx-qirE9K1Sdy2W2SyYWNo_wY_Q'  # Replace with your folder ID

# Read the last tweeted frame index from the file
with open('last_tweet_index.txt', 'r') as f:
    last_tweet_index = int(f.read())

# Retrieve photo files from Google Drive
file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()

# Sort the file list by title
file_list.sort(key=lambda x: x['title'])

# Tweet the next two frames
for i in range(last_tweet_index, min(last_tweet_index + 2, len(file_list))):
    file = file_list[i]
    # Get the image file from Google Drive as a file-like object
    response = requests.get(file['webContentLink'])
    image_file = BytesIO(response.content)

    # Upload the image to Twitter
    media = api.media_upload(filename=file['title'], file=image_file)

    # Create the caption
    caption = f"#DevaraGlimpse - Frame {i+1} of {len(file_list)} Frames"

    # Tweet with the image and caption
    tweet = client.create_tweet(text=caption, media_ids=[media.media_id])

    print(f"Tweeted image: {file['title']}")

# Update the last tweeted frame index in the file
with open('last_tweet_index.txt', 'w') as f:
    f.write(str(min(last_tweet_index + 2, len(file_list))))