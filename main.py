import tweepy
import requests
import time
import openai
import random
# import cv2
import urllib
import numpy as np
# import matplotlib.pyplot as plt
from gingerit.gingerit import GingerIt
import dotenv
from dotenv import load_dotenv
import os
from datetime import date
import math
import textwrap
import firebase_admin
from firebase_admin import credentials, db


load_dotenv()
cred = credentials.Certificate("quotetwitterbotdb-firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://quotetwitterbotdb-default-rtdb.firebaseio.com'
})

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET_KEY = os.getenv("TWITTER_API_SECRET_KEY")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
TWITTER_CLIENT_ID = os.getenv("TWITTER_CLIENT_ID")
TWITTER_CLIENT_SECRET = os.getenv("TWITTER_CLIENT_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_SECRET_ACCESS_TOKEN = os.getenv("TWITTER_SECRET_ACCESS_TOKEN")
QUOTE_API = os.getenv("QUOTE_API")
OPENAI_API_SECRET_KEY = os.getenv("OPENAI_API_SECRET_KEY")

openai.api_key = OPENAI_API_SECRET_KEY

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_SECRET_ACCESS_TOKEN)
api = tweepy.API(auth, wait_on_rate_limit=True)
parser = GingerIt()
prompt_suffixes = ["unreal engine, ultra-details, 16k", "synthwave cyberpunk, cool, contrasting, motivating, 16k", "fantasy art, ultra details, 16k, motivating, inspiring"]

def get_quote_of_day(index: int):
    response = requests.get(f"{QUOTE_API}/get-IK-quotes/{index}")
    response = response.json()
    quote = response["quote"]
    corrected_quote = parser.parse(quote)['result']
    print(corrected_quote)

    response_from_chatgpt = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Describe a scenic, awe-inspiring and motivational image, without any specifics about any country and not on set on a mountain, that depicts the following quote in 10 simple words: '{corrected_quote}'. The image should have no caption.",
    temperature=0.6,
    max_tokens=256,
    )
    
    image_desc = response_from_chatgpt["choices"][0]
    print(image_desc)

    # response_from_dalle = openai.Image.create(
    # prompt=f"{random.choice(prompt_suffixes)} {image_desc}",  # random.choice(list_of_dalle_prompts)
    # n=1,
    # size="1024x1024"
    # )

    # print(type(response_from_dalle))
    response_from_deepai = requests.post(
        "https://api.deepai.org/api/fantasy-world-generator",
        data={
            'text': f'{image_desc}, {prompt_suffixes[2]}', #{random.choice(prompt_suffixes)}
            'grid_size': "1",
        },
        headers={'api-key': 'a60598a5-c4e9-4f29-aad2-a2bb0ff896f1'}
    )
            # 'width': "1536",
            # 'height': "1152",
    # print(response_from_deepai.json())
    
    response_from_deepai = dict(response_from_deepai.json())
    # image_url1 = response_from_dalle['data'][0]['url']
    image_url2 = response_from_deepai['output_url']

    # img_data1 = requests.get(image_url1).content
    # suffix = time.strftime("%Y%m%d-%H%M%S")

    # with open(f'assets/images_for_tweeting/image_{suffix}.jpg', 'wb') as handler:
    #     handler.write(img_data1)
    
    # img1 = cv2.imread(f'assets/images_for_tweeting/image_{suffix}.jpg', cv2.IMREAD_COLOR) 
    # cv2.imshow('Image1', img1)

    img_data2 = requests.get(image_url2).content
    suffix = time.strftime("%Y%m%d-%H%M%S")

    with open(f'assets/images_for_tweeting/image_{suffix}.jpg', 'wb') as handler:
        handler.write(img_data2)
    
    image2_path = f'assets/images_for_tweeting/image_{suffix}.jpg'
    # img2 = cv2.imread(image2_path, cv2.IMREAD_COLOR) 
    # cv2.imshow('Image2', img2)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    corrected_quote = f"'{corrected_quote}' \n--- @ImranKhanPTI of @PTIofficial"
    return corrected_quote, image2_path

def post_tweet(quote, image_path, api):
    media = api.media_upload(image_path)
    twitter_handle = '@KaptaanQuotes'
    max_tweet_limit = 280
    tweet_length = len(quote)
    if tweet_length <= max_tweet_limit:
        post_result = api.update_status(status=quote, media_ids=[media.media_id])
    elif tweet_length > max_tweet_limit:
        tweet_length_limit = tweet_length/280
        tweet_chunk_length = (tweet_length/math.ceil(tweet_length_limit)) + len(twitter_handle)
        tweet_chunks = textwrap.wrap(quote,  math.ceil(tweet_chunk_length), break_long_words=False)

        # iterate over the chunks 
        for x, chunk in zip(range(len(tweet_chunks)), tweet_chunks):
            if x == 0:
                chunk = f"(1 of {len(tweet_chunks)}) {chunk}..."
                post_result = api.update_status(status=chunk, media_ids=[media.media_id])
            elif x < len(tweet_chunks)-1:
                chunk = f"({x+1} of {len(tweet_chunks)}) {chunk}..."
                post_result = api.update_status(status=chunk, in_reply_to_status_id=post_result.id, auto_populate_reply_metadata=True)
            else:
                chunk = f"({x+1} of {len(tweet_chunks)}) {chunk}"
                post_result = api.update_status(status=chunk, in_reply_to_status_id=post_result.id, auto_populate_reply_metadata=True)

    print(post_result)
    print(20*"=", "Tweet Successful", 20*"=")
    return quote

# TWEET_INDEX = os.getenv("TWEET_INDEX")
# TWEET_INDEX = (date.today()-START_DATE).days
# TWEET_INDEX = 53
tweet_index_ref = db.reference('/tweets/TWEET_INDEX')
print(tweet_index_ref)
TWEET_INDEX = tweet_index_ref.get()

if TWEET_INDEX is None:
    TWEET_INDEX = 0

print(TWEET_INDEX)

quote, image_path = get_quote_of_day(TWEET_INDEX)
post_tweet(quote, image_path, api)
# dotenv_file = dotenv.find_dotenv()
TWEET_INDEX += 1
tweet_index_ref.set(TWEET_INDEX)
# dotenv.set_key(dotenv_file, "TWEET_INDEX", f'{int(TWEET_INDEX)+1}')
