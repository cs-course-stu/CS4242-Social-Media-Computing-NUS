from classify.textprocessor import TextProcessor
import pandas as pd
import numpy as np
from fast_bert.prediction import BertClassificationPredictor

class TextClassifier:

    def __init__(self, in_dir, dictionary_file, hashtag_file, input_file, model_dir="model_out"):
        self.in_dir = in_dir
        self.hashtag = set()
        self.dictionary = {}
        self.dictionary_file = dictionary_file
        self.hashtag_file = hashtag_file
        self.input_file = input_file
        self.train_file = None
        self.valid_file = None
        self.model_dir = model_dir

    def load_raw_data(self):
        textprocessor = TextProcessor(
            self.in_dir, self.dictionary_file, self.hashtag_file)
        textprocessor.load_dictioanry()
        textprocessor.load_hashtag()
        dat = pd.read_csv(
            self.in_dir + '/' + self.input_file, header=None)

        dat.columns = ['tweet', 'hashtag']
        # n = len(dat)
        # nlist = range(0,n)
        dat['id'] = None
        dat = dat[['id', 'tweet', 'hashtag']]

        total = ['id', 'tweet', 'hashtag']
        total = total + list(textprocessor.hashtag)
        dat = dat.reindex(columns=list(total), fill_value=0)
        dat['tweet'] = dat['tweet'].apply(textprocessor.cleanup)
        dat['tweet'] = dat['tweet'].apply(textprocessor.informal_norm)

        dat['hashtag'] = dat['hashtag'].apply(textprocessor.del_hashtag)
        dat = dat.drop(dat[dat['hashtag'].map(len) <
                           1].index).reset_index(drop=True)

        dat['tweet'] = dat['tweet'].apply(textprocessor.drop_tweet)
        dat = dat.drop(dat[dat['tweet'].map(len) <
                           1].index).reset_index(drop=True)
        n = len(dat)
        nlist = range(0, n)
        dat['id'] = nlist

        # assign label
        for i in range(len(dat['hashtag'])):
            tmp_list = dat['hashtag'][i].split(",")
            for j in range(len(tmp_list)):
                tmp_list[j] = tmp_list[j].replace(' ', '')
                dat[tmp_list[j]][i] = 1
        return dat.drop(columns=['hashtag'])

    def split_data(self,data):
        self.train_file, self.valid_file = np.split(
            data.sample(frac=1), [int(.7*len(data))])
        
    def save_to_file(self):
        self.train_file.to_csv(self.in_dir + '/' +
                               "train.csv", index=False, header=False)
        self.valid_file.to_csv(self.in_dir + '/' +
                               "valid.csv", index=False, header=False)
            
    def predict(self, text):
        predictor = BertClassificationPredictor(
            model_path=self.in_dir + '/' +self.model_dir,
            label_path=self.in_dir + '/labels',  # location for labels.csv file
            multi_label=True,
            # model_type='xlnet',
            do_lower_case=True)
        prediction = predictor.predict(str(text))[:7]
        rst_list = []
        for i in range(len(prediction)):
            rst_list.append(" #" +str(prediction[i][0]))
        return rst_list

if __name__ == '__main__':
    textclassifier = TextClassifier(
        '/Users/wangyifan/Google Drive/multi-label-classification', 'dictionary.txt', 'hashtag.txt', 'input.train.text.csv')
    
    # data = textclassifier.load_raw_data()
    # print(data[34234:34235])
    string = "fuck trump"
    print(string)
    print(textclassifier.predict(string))
