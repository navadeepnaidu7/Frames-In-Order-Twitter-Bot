import os
import tweepy

# Enter API tokens below
bearer_token = os.environ.get('BEARER_TOKEN')
consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

# V1 Twitter API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# V2 Twitter API Authentication
client = tweepy.Client(
    bearer_token,
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
    wait_on_rate_limit=True,
)

# Upload image to Twitter. Replace 'filename' your image filename.
media_id = api.media_upload(filename="frame.png").media_id_string
print(media_id)

# Text to be Tweeted
text = "Hello Twitter! #Devara"

# Send Tweet with Text and media ID
client.create_tweet(text=text, media_ids=[media_id])
print("Tweeted!")