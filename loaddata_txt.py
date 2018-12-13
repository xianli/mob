import datetime
import loaddata

#file="cover_hour"
#timeformat="%Y-%m-%d %H:%M:%S"
file="cover_day"
timeformat="%Y/%m/%d %H:%M"
with open("data/{}.txt".format(file)) as f:
    allline=[one.strip("\r\n").split("\t") for one in f.readlines()]

for one in allline[1:]:
    one[1]=datetime.datetime.strptime(one[1],timeformat)

print(len(allline))

clearline=[]
defaut=['MSISDN', 'VERSION_DATE', -47, 'RSRP_105_CNT', 100, 'RSRP_110_CNT', 100, 40, 0, 100, 'SIXDB3NEI', 0, 0, 'TAU_SUC_CNT',0, 'PAGING_CNT', 100, 0, 0, 0, 'PHR0_CNT', 0]

#计算有效数据的平均值
defaultsum=[0]*len(defaut)
defaultcount=[0]*len(defaut)

for one in allline[1:]:
    for c in range(2,len(one)):
        if one[c]!="":
            defaultsum[c]+=float(one[c])
            defaultcount[c]+=1
for c in range(2,len(defaultcount)):
    defaultcount[c]=defaultcount[c]/defaultsum[c]
for c in range(2,len(defaut)):
    defaut[c]=defaultsum[c]
#计算有效数据的平均值  end

#修复数据
for one in allline[1:]:
    has_ept=False
    for c in range(len(one)):
        if one[c]=="":
            if type(defaut[c])==str:
                has_ept=True
                break
            else:
                one[c]=defaut[c]
    if has_ept==False:
        clearline.append(one)
print(len(clearline))
#修复数据 end
yhlist=loaddata.loadData("data/用户满意度.xlsx")

users_sat={}
for one in yhlist[1]:
    one_num=[int(o) if o!=None else 10 for o in one[1:]]
    users_sat[one[0]]={"scro":one_num,"his":[]}
print(len(users_sat))

#和用户满意度配对
for one in clearline:
    if one[0] in users_sat:
        onenum=[float(o) if type(o)==str and o.isdigit() else o for o in one[1:]]
        users_sat[one[0]]["his"].append(onenum)

for one in list(users_sat.keys()):
    if len(users_sat[one]["his"])==0:
        del users_sat[one]

print(len(users_sat))

import json
from bson import json_util
users_sat={"head":allline[0],"data":users_sat}
with open("processed/users_sat_{}.json".format(file),"w") as f:
    json.dump(users_sat,f,default=json_util.default)