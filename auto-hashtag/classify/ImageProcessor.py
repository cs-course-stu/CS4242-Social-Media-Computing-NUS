import argparse
import os
import torchvision.datasets as datasets
import tensorflow as tf
from classify.utils import preprocess_for_eval
from classify.pnasnet import build_pnasnet_large, pnasnet_large_arg_scope
import numpy as np
import cv2
from urllib import request
import shutil

class ImageProcessor():
    def __init__(self,ckpt=r'..\model\model.ckpt',valdir="../upload",img_folder_name='test'):
        self.headers = {
          "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36',
          # "host": 'www.eeeeee.com',
          "Referer": 'XXXXXXMMMMMMMMMMMMMMM'
        }
        # parser = argparse.ArgumentParser()
        # parser.add_argument('--valdir', type=str, default=valdir,
        #                     help='path to ImageNet val folder')
        # parser.add_argument('--image_size', type=int, default=256,
        #                     help='image size')
        # self.args = parser.parse_args()
        self.valdir = valdir
        self.image_size = 256
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'
        self.img_folder_name = img_folder_name
        self.ckpt = ckpt


    def pic_open(self,url):
        req = request.Request(url=url, data=None, headers=self.headers, method="GET")
        response = request.urlopen(req)
        pic = response.read()
        return pic

    def prepare_data(self,url_list):
        img_folder = os.path.join(self.valdir, self.img_folder_name)
        shutil.rmtree(self.valdir)
        os.mkdir(self.valdir)
        os.mkdir(img_folder)

        for idx, url in enumerate(url_list):
          with open(f'{img_folder}/{idx}.jpg', 'wb') as f:
            try:
              img = self.pic_open(url)
              f.write(img)
            except ValueError:
              print("Fail for: " + url)
        imgs = os.listdir(img_folder)
        os.mkdir(img_folder+"npy")

        for img_name in imgs:
          img = cv2.imread(os.path.join(img_folder,img_name)).astype(np.float32)
          img = cv2.resize(img,(224,224))
          img = img[np.newaxis,:]
          img = img[np.newaxis,:]
          for i in range(4):
            img = np.concatenate([img,img],axis=1)
          np.save(os.path.join(img_folder+"npy",img_name[:-4]+".npy"),img)

    def predict(self):
        slim = tf.contrib.slim
        # self.prepare_data(url_list)

        image_ph = tf.placeholder(tf.uint8, (None, None, 3))
        image_proc = preprocess_for_eval(image_ph, self.image_size, self.image_size)
        images = tf.expand_dims(image_proc, 0)
        with slim.arg_scope(pnasnet_large_arg_scope()):
          logits, _ = build_pnasnet_large(images, num_classes=1001, is_training=False)

        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        sess = tf.Session(config=config)
        ckpt_restorer = tf.train.Saver()
        ckpt_restorer.restore(sess, self.ckpt)

        # c1, c5 = 0, 0
        val_dataset = datasets.ImageFolder(self.valdir)
        with open("../model/id2name", "r", encoding='utf-8') as f:
          names = f.readlines()
        out_list = []
        for i, (image, _) in enumerate(val_dataset):
          logits_val = sess.run(logits, feed_dict={image_ph: image})
          top5 = logits_val.squeeze().argsort()[::-1][:5]
          # print(logits_val.squeeze().argsort()[::-1])
          # the probability!!! here.
          # print(logits_val.squeeze()[top5[0]],logits_val.squeeze()[top5[1]],logits_val.squeeze()[top5[2]])
          top5_name = []
          for id in top5:
              top5_name.append(names[id].split("\t")[2])
          # print(top5_name)
          out_list.append([" #"+ x for x in top5_name[:4]])


        return out_list  # get top3


if __name__ == '__main__':
    # url_list = ["https://pbs.twimg.com/media/ETlgloVUwAAldTH?format=jpg&name=large","https://pbs.twimg.com/media/ETlgloVUwAAldTH?format=jpg&name=large"]
    imageProcessor = ImageProcessor(ckpt=r'E:\PycharmProject\CS4242-Social-Media-Computing-NUS-master\model\model.ckpt')
    print(imageProcessor.predict())
