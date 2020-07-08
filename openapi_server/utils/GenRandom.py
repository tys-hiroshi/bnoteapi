# coding: UTF-8

import random

class GenRandom:
    def __init__(self):
        pass
    
    def generate_random_index(self, max_indexnum):

        # ランダムに複数の要素を選択　重複なし
        return random.sample(list(range(0, max_indexnum)), k=max_indexnum)

