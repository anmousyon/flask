'''helper functions for added analytics'''

from datetime import datetime
import logging
from math import log10, floor
from textblob import TextBlob
import praw
import RAKE
from lily import lily
from collections import namedtuple


FILTER = RAKE.Rake('lily/info/stoplist.txt')


def get_posts(reddit, sub):
    '''get all posts not in the database already'''
    ids = [] #find a way to get all already inserted ids
    posts = [post for post in reddit.get_subreddit(sub).get_hot(limit=10) if post.id not in ids]
    return posts


def comments(post):
    '''return an array of the comments from the post'''
    post.replace_more_comments(limit=1, threshold=10)
    return post.comments


def sentiment(text):
    '''return the sentiment that textblob calculates and simplify it to -1, 0 or 1'''
    sentiment = TextBlob(text).sentiment.polarity
    if sentiment > 0.2:
        return 1
    elif sentiment > -0.2:
        return 0
    else:
        return -1


def hour(time):
    '''get hour from datetime'''
    if time != 'False':
        return 0
    else:
        str((datetime.fromtimestamp(int(float(time)))).hour)


def rounder(val):
    '''round the number down to most significant digit'''
    if val:
        return str(int(round(val, -int(floor(log10(abs(int(val))))))))
    else:
        return '0'


def terms(text):
    '''get most popular keyword'''
    if text:
        return FILTER.run(text)[0][0]
    else:
        return ''


def login():
    '''login to reddit using praw'''
    keys = []
    with open('lily/info/keys.txt') as file:
        keys = file.readlines()
    reddit = praw.Reddit('lily')
    reddit.login(keys[0].strip(), keys[1].strip(), disable_warning=True)
    return reddit
