import os
import pandas as pd

"""Reference
https://www.webopedia.com/quick_ref/Twitter_Dictionary_Guide.asp
https://www.socialmediatoday.com/content/top-twitter-abbreviations-you-need-know
https://digiphile.info/2009/06/11/top-50-twitter-acronyms-abbreviations-and-initialisms/
https://bitrebels.com/social/twitter-dictionary-35-twitter-abbreviations/
"""
class TextProcessor:
    """ class TextProcessor is a class dealing with crawling tweets
    Args:
        in_dir: working directory
        consumer_key: Twitter API: consumer_key
        consumer_secret: Twitter API: consumer_secret
        access_token: Twitter API: access_token
        access_token_secret: Twitter API: access_token_secret
    """

    def __init__(self, in_dir):
        self.in_dir = in_dir
        self.hashtag = set()
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
            if line[0].lower() not in self.dictionary:
                self.dictionary[line[0].lower()] = line[1].replace('\n', '').lower()
        print('load dictionary successfully')

    """ load local hashtag and build set
    """

    def _load_hashtag(self):
        print('loading hashtag...')
        if (not os.path.exists(self.in_dir)):
            print("wrong file path!")
            sys.exit(2)
        f = open(self.in_dir+"/"+'hashtag.txt')

        # load dictionary and build index
        for line in iter(f):
            if line.lower() not in self.hashtag:
                self.hashtag.add(line.lower().replace('\n','').replace('#',''))
        print('load hashtag successfully')

    """ Irrelevant hashtag filtering
    Args:
        text: text to be filtered
    
    Returns:
        ' '.join(rst): filtered hashtag
    """

    def _del_hashtag(self, text):
        tmp_list = str(text).split(',')
        rst = []
        for i in range(len(tmp_list)):
            if (tmp_list[i].lower().replace(' ', '') in self.hashtag):
                rst.append(tmp_list[i].lower().replace(' ', ''))
        return ', '.join(rst)

    """ Informal language normalization
    Args:
        text: text to be normailzed
    
    Returns:
        ' '.join(tmp_list): normalized text
    """

    def _informal_norm(self,text):
        tmp_list = text.split()
        for i in range(len(tmp_list)):
            if (tmp_list[i].lower() in self.dictionary):
                tmp_list[i] = self.dictionary[tmp_list[i].lower()]
        return ' '.join(tmp_list)

    """ Irrelevant text tokens filtering
    Args:
        text: text to be filtered
    
    Returns:
        text: filtered text
    """

    def _cleanup(self, text):
        # drop http[s]://*
        text = re.sub(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', str(text))

        # drop something liek @EP_President
        text = re.sub(u"\@.*?\s", '', str(text))

        # drop # of hashtag within sentence
        text = text.replace('#',' ')

        #  remove emojis
        text = text.encode('ascii', 'ignore').decode('ascii')
        
        return text

    """ drop tweets whose length <= 3
    Args:
        text: text to be filtered
    
    Returns:
        text: filtered text
    """

    def _drop_tweet(self, text):
        if (len(text.split()) <= 3):
            return ""
        else:
            return text

if __name__ == '__main__':
    textprocessor = TextProcessor('/Users/wangyifan/Desktop')
    textprocessor._load_hashtag()
    print(textprocessor._del_hashtag(
          "i am wang "))