# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 18:38:28 2020

@author: gaeeeemi
"""

import numpy as np
import os

#일관된 출력을 위한 유사난수 초기화
np.random.seed(42)

#맷플롯립 설정
%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

#그래프 이미지를 저장할 폴더 설정
PROJECT_ROOT_DIR = '.'
CHAPTER_ID = "decision_trees"

def image_path(fig_id):
    return os.path.join(PROJECT_ROOT_DIR, 'images', CHAPTER_ID, fig_id)

def save_fig(fig_id, tight_layout = True):
    if tight_layout:
        plt.tight_layout()
    plt.savefig(image_path(fig_id) + '.png', format = 'png', dpi = 300)
    
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

iris = load_iris()#sklearn 모듈안의 붓꽃 데이터셋 불러오기
X = iris.data[:, 2:]#데이터셋의 2,3번째 column속성만 불러오기
y = iris.target#데이터셋의 클래스

tree_clf = DecisionTreeClassifier(max_depth = 2, random_state = 42)#결정트리 모델 불러오기
tree_clf.fit(X, y)

from sklearn.tree import export_graphviz
from graphviz import Source

#결정트리 그래프를 그려줄 함수
export_graphviz(
                tree_clf,
                out_file = image_path('iris_tree.dot'),
                feature_names = ['꽃잎 길이(cm)', '꽃잎 너비(cm)'],
                class_names = iris.target_names,
                rounded = True,
                filled = True
                )

with open('images/decision_tress/iris_tree.dot')as f:
    dot_graph = f.read()    
    dot = graphviz.Source(dot_graph)
    dot.format = 'png'
    dot.render(filename='iris_tree', directory='images/decision_trees', cleanup=True)
dot