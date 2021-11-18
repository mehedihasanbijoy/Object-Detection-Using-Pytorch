# -*- coding: utf-8 -*-
"""custom_dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DLRmr99ynKtIMEu7DT0NmjYSAKhKg8D3
"""

from torch_snippets import *
from PIL import Image
import glob
import os
from utils import preprocess_image

class OpenDataset(torch.utils.data.Dataset):
    w, h = 224, 224
    def __init__(self, df, label2target, image_dir):
        self.label2target = label2target
        self.image_dir = image_dir
        self.files = glob.glob(self.image_dir+'/*')
        self.df = df
        self.image_infos = self.df.ImageID.unique()
        # self.image_infos = df.ImageID.unique()

    def __getitem__(self, ix):
        image_id = self.image_infos[ix]
        img_path = find(image_id, self.files)
        img = Image.open(img_path).convert("RGB")
        img = np.array(img.resize((self.w, self.h), resample=Image.BILINEAR))/255.
        # data = df[df['ImageID'] == image_id]
        data = self.df[self.df['ImageID'] == image_id]
        labels = data['LabelName'].values.tolist()
        data = data[['XMin','YMin','XMax','YMax']].values
        data[:,[0,2]] *= self.w
        data[:,[1,3]] *= self.h
        boxes = data.astype(np.uint32).tolist() 
        target = {}
        target["boxes"] = torch.Tensor(boxes).float()
        target["labels"] = torch.Tensor([self.label2target[i] for i in labels]).long()
        img = preprocess_image(img)
        return img, target

    def collate_fn(self, batch):
        return tuple(zip(*batch)) 

    def __len__(self):
        return len(self.image_infos)





