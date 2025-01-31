# Implementation of Time Series Classification from Scratch with Deep Neural Networks: A Strong Baseline (2016, arXiv) in PyTorch.
# The scripts are provided by https://github.com/aybchan/time-series-classification 
import pandas as pd
import numpy as np
import os
from scipy.io.arff import loadarff
import torch
from torch.utils.data import Dataset

import os
curdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class Data(Dataset):
    """
    Implements a PyTorch Dataset class
    """
    def __init__(self,dataset,testing):
        train_data = pd.DataFrame(
            loadarff(curdir + '/examples/datasets/{}_TRAIN.arff'.format(dataset))[0])
        dtypes = {i:np.float32 for i in train_data.columns[:-1]}
        dtypes.update({train_data.columns[-1]: np.int})
        train_data = train_data.astype(dtypes)

        self.x = train_data.iloc[:,:-1].values
        self.y = train_data.iloc[:,-1].values

        self.mean = np.mean(self.x, axis=0)
        self.std  = np.std(self.x, axis=0)
        print("Current working directory1: {0}".format(os.getcwd()))
        if testing:
            test_data  = pd.DataFrame(
                loadarff(curdir + '/examples/datasets/{}_TEST.arff'.format(dataset))[0])
            dtypes = {i:np.float32 for i in test_data.columns[:-1]}
            dtypes.update({test_data.columns[-1]: np.int})
            test_data  = test_data.astype(dtypes)

            self.x = test_data.iloc[:,:-1].values
            self.y = test_data.iloc[:,-1].values

        class_labels = np.unique(self.y)
        if (class_labels != np.arange(len(class_labels))).any():
            new_labels = {old_label: i for i,old_label in enumerate(class_labels)}
            self.y = [new_labels[old_label] for old_label in self.y]

        self.x = (self.x - self.mean) / self.std

    def __len__(self):
        return len(self.y)

    def __getitem__(self,idx):
        x = torch.Tensor([self.x[idx]]).float()
        y = torch.Tensor([self.y[idx]]).long()
        return x,y