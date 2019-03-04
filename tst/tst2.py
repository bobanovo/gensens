TrendPos=[]
TrendTrend=[]

TrendPlan = {10:-1, 20:1, 30:0, 35:-1}
for _tmp1 in TrendPlan:
    TrendPos.append(_tmp1)
    TrendTrend.append(TrendPlan[_tmp1])

for x in TrendPos:
    print (x)

for x in TrendTrend:
    print (x)
