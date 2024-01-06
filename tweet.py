import tweepy
import os
import random

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

# Determine image folder relative to the script's location
script_dir = os.path.dirname(__file__)
image_folder = os.path.join(script_dir, "images")  # Assuming images are in the "images" subfolder

image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

# Tweet with each image, caption, and random hashtag
for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)

    media = api.media_upload(image_path)

    caption = f"test tweet with image! {random.choice(['#JrNTR', '#Devara', '#Bot'])}"

    tweet = client.create_tweet(text=caption, media_ids=[media.media_id])

    print(f"Tweeted image: {image_file}")