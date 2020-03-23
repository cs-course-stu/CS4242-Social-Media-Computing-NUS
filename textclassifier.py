from textprocessor import TextProcessor
import pandas as pd


class TextClassifier:

    def __init__(self, in_dir, dictionary_file, hashtag_file, train_file):
        self.in_dir = in_dir
        self.hashtag = set()
        self.dictionary = {}
        self.dictionary_file = dictionary_file
        self.hashtag_file = hashtag_file
        self.train_file = train_file


    def load_raw_data(self):
        textprocessor = TextProcessor(
            self.in_dir, self.dictionary_file, self.hashtag_file)
        textprocessor.load_dictioanry()
        textprocessor.load_hashtag()
        dat = pd.read_csv(
            self.in_dir + '/' + self.train_file, header=None)
        dat.columns = ['tweet', 'hashtag']
        # add each hashtag to the data as label
        total = ['tweet', 'hashtag']
        total = total + list(textprocessor.hashtag)
        dat = dat.reindex(columns=list(total), fill_value=0)

        # preprocessing
        dat['tweet'] = dat['tweet'].apply(textprocessor.cleanup)
        dat['tweet'] = dat['tweet'].apply(textprocessor.informal_norm)
        dat['hashtag'] = dat['hashtag'].apply(textprocessor.del_hashtag)
        dat = dat.drop(dat[dat['hashtag'].map(len) <
                           1].index).reset_index(drop=True)
        dat['tweet'] = dat['tweet'].apply(textprocessor.drop_tweet)
        dat = dat.drop(dat[dat['tweet'].map(len) <
                           1].index).reset_index(drop=True)
        
        # assign every hashtag to the label
        for i in range(len(dat['hashtag'])):
            tmp_list = dat['hashtag'][i].split(",")
            for j in range(len(tmp_list)):
                tmp_list[j] = tmp_list[j].replace(' ', '')
                dat[tmp_list[j]][i] = 1
        return dat


        def create_input(self):
            pass

if __name__ == '__main__':
    textclassifier = TextClassifier(
        '/Users/wangyifan/Desktop', 'dictionary.txt', 'hashtag.txt', 'input.train.text.csv')
    
    data = textclassifier.load_raw_data()
    print(data[34234:34235])
