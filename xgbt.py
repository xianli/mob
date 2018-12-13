from bson import json_util
import json
import pickle

with open("processed/users_sat_cover_day.json","r") as f:
    data=json.load(f, object_hook=json_util.object_hook)

import numpy as np

from sklearn.model_selection import train_test_split
import xgboost as xgb

src=[]
tgt=[]
for k in data["data"]:
    one=data["data"][k]
    if one["scro"][0] >10:
        continue
    scro=0
    if one["scro"][0]>8:
        scro=2
    elif one["scro"][0]>6:
        scro=1
    tgt.append(scro)
    src.append(one["his"][0][1:])
print(len(src))
X_train, X_test, y_train, y_test = train_test_split(src, tgt)
X_train, X_test, y_train, y_test=np.array(X_train),np.array(X_test),np.array(y_train),np.array(y_test)

dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test)

params = { 'booster': 'gbtree',
           'objective': 'multi:softmax', # 多分类的问题
            'num_class': 3, # 类别数，与 multisoftmax 并用
            'gamma': 0.2, # 用于控制是否后剪枝的参数,越大越保守，一般0.1、0.2这样子。
           #'max_depth': 12, # 构建树的深度，越大越容易过拟合
           "max_leaf_nodes":80,
            'lambda': 2, # 控制模型复杂度的权重值的L2正则化项参数，参数越大，模型越不容易过拟合。
            'subsample': 0.7, # 随机采样训练样本
            'colsample_bytree': 0.7, # 生成树时进行的列采样
           'min_child_weight': 4,
           'silent': 1, # 设置成1则没有运行信息输出，最好是设置为0.
           'eta': 0.007, # 如同学习率
            'seed': 1000,
           'nthread': 4, # cpu 线程数
           }

estimator=xgb.train(params,dtrain,10)

leave_id = estimator.predict(dtest)
diff=np.abs(leave_id-y_test)
print(diff)
print((np.average(diff)))
print(np.sqrt(np.sum(np.power(diff,2))/len(diff)))
prdcount=[0]*3
for i in diff:
    prdcount[int(i)]+=1
for i in prdcount:
    print("{0:.2f}".format(float(i)/len(diff)))

with open("processed/xgb.pkl","wb") as f:
    pickle.dump(estimator,f)