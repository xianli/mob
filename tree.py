from bson import json_util
import json
import pickle

with open("processed/users_sat_cover_day.json","r") as f:
    data=json.load(f, object_hook=json_util.object_hook)

import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

src=[]
tgt=[]
for k in data["data"]:
    one=data["data"][k]
    if one["scro"][1] >10:
        continue
    tgt.append(one["scro"][1])
    src.append(one["his"][0][1:])

X_train, X_test, y_train, y_test = train_test_split(src, tgt,test_size=200)
X_train, X_test, y_train, y_test=np.array(X_train),np.array(X_test),np.array(y_train),np.array(y_test)

estimator = DecisionTreeClassifier(max_leaf_nodes=80)
estimator.fit(X_train, y_train)

leave_id = estimator.predict(X_test)
diff=np.abs(leave_id-y_test)
print(diff)
print((np.average(diff)))
prdcount=[0]*10
for i in diff:
    prdcount[int(i)]+=1
for i in prdcount:
    print("{0:.2f}".format(float(i)/len(diff)))

with open("processed/tree.pkl","wb") as f:
    pickle.dump(estimator,f)