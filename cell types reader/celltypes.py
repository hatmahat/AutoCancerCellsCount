"""
Cell types reader from file names
Written by Mahatma Wisesa
"""
import os
import numpy as np
import re

class CountTypes:

    def __init__(self, ROOT_DIR, CHILD):
        self.ROOT_DIR = ROOT_DIR
        self.CHILD = self.ROOT_DIR+f"\\{CHILD}"
        self.file_names = []
        self.preprocessed = []
        self.preprocessed_1D = []
        self.uniq_dict = {}
        self.blast_vs_nonblast_dict = {
            'Non-Limfoblas':0,
            'Limfoblas':0
        }

    def get_file_names(self):
        return self.file_names

    def get_preprocessed(self):
        return self.preprocessed

    def preprocessed_1D(self):
        return self.preprocessed_1D

    def get_uniq_dict(self):
        return self.uniq_dict

    def get_blast_vs_nonblast(self):
        return self.blast_vs_nonblast_dict

    def read_file_names(self):
        self.file_names = [
            file_name.replace(".jpg", "") for file_name in os.listdir(self.CHILD)
        ]

    def count_cells(self):
        self.preprocessed = [
            re.sub("[\(\[].*?[\)\]]", "", file_name).split(" ")[1:] for file_name in self.file_names if len(file_name.split(' ')) > 1
        ]
        # ubah dari list 2d ke 1 d
        for cells in self.preprocessed:
            for cell in cells:
                if cell != '':
                    self.preprocessed_1D.append(cell)
        
        # buat keys untuk dict setiap nama uniq
        uniqs = np.unique(np.array(self.preprocessed_1D))
        for uniq_name in uniqs:
            self.uniq_dict[uniq_name] = 0

        for cell in self.preprocessed_1D:
            self.uniq_dict[cell] += 1

        for cell, total in self.uniq_dict.items():
            if cell != 'B':
                self.blast_vs_nonblast_dict['Non-Limfoblas'] += total
            else:
                self.blast_vs_nonblast_dict['Limfoblas'] = total
