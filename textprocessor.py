from __future__ import print_function, division
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import os
import copy
from torch.utils.data import Dataset, DataLoader
from PIL import Image
from random import randrange
import torch.nn.functional as F
from sklearn.metrics import roc_curve, auc
# import nlpaug.augmenter.char as nac
#import nlpaug.augmenter.word as naw
# import nlpaug.flow as naf
# from nlpaug.util import Action
import pandas as pd

# https://www.webopedia.com/quick_ref/Twitter_Dictionary_Guide.asp
# https://www.socialmediatoday.com/content/top-twitter-abbreviations-you-need-know
# https://digiphile.info/2009/06/11/top-50-twitter-acronyms-abbreviations-and-initialisms/
# https://bitrebels.com/social/twitter-dictionary-35-twitter-abbreviations/

class TextProcessor:
    """ class TextProcessor is a class dealing with crawling tweets
    Args:
        in_dir: working directory
        consumer_key: Twitter API: consumer_key
        consumer_secret: Twitter API: consumer_secret
        access_token: Twitter API: access_token
        access_token_secret: Twitter API: access_token_secret
    """

    def __init__(self, in_dir ):
        self.in_dir = in_dir
        self.dictionary = {}

    """ load local dictionary and build index
    """
    
    def _load_dictioanry(self):
        print('loading dictionary...')
        if (not os.path.exists(self.in_dir)):
            print("wrong file path!")
            sys.exit(2)
        f = open(self.in_dir+"/"+'dictionary.txt')

        # load dictionary and build index
        for line in iter(f):
            line = line.split(' ', 1)
            #print(line[0].lower())
            if line[0].lower() not in self.dictionary:
                self.dictionary[line[0].lower()] = line[1].replace('\n', '').lower()

    def _cleanup(self, text):
        # drop http[s]://*
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','',text)

        # drop something liek @EP_President
        text = re.sub(u"\@.*?\s", '', text)

        # drop # of hashtag within sentence
        text = text.replace('#',' ')

        #  remove emojis
        text = text.encode('ascii', 'ignore').decode('ascii')
        
        return text
