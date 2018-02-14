# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# calculate the length of a chinese word in different encoding method
wordlen = len('年')
def cal(s):
    # transform salary into float type(RMB/month).
    if str(s) == 'nan':
        return(s)
    pay,freq = s.split('/')
    if freq == '年':
        count = 12
    elif freq == '月':
        count = 1
    else:
        count = 1/22.5
    if pay[len(pay)-1*wordlen:] in ['上', '下']:
        pay = pay[0:len(pay)-2*wordlen]
    if pay[len(pay)-1*wordlen:] == '万':
        pay = pay[0:len(pay)-1*wordlen].split('-')
        pay = np.mean(list(map(float,pay))) * 10000
    elif pay[len(pay)-1*wordlen:] == '千':
        pay = pay[0:len(pay)-1*wordlen].split('-')
        pay = np.mean(list(map(float,pay))) * 1000
    elif pay[len(pay)-1*wordlen:] == '元':
        pay = pay[0:len(pay)-1*wordlen].split('-')
        pay = np.mean(list(map(float,pay)))
    else:
        return(s)
    return(pay/count)


def refine(jobs):
    # drop duplicated data, and sort by salary.
    unijobs = jobs[['job', 'company', 'salary']]
    unijobs = unijobs.drop_duplicates()
    unijobs = unijobs[unijobs.job.str.contains(r'.*?数据.*', na = False)]
    unijobs = unijobs.sort_values(by = 'salary', ascending = False)
    return(unijobs)

def groupStat(jobs, by, values = 'salary'):
    # group statistics
    grouped = jobs.dropna().groupby(by)[values]
    groupMean = pd.DataFrame(grouped.mean()).sort_values(by = values, ascending = False)
    groupCount = pd.DataFrame(grouped.count()).sort_values(by = values, ascending = False)
    plt.figure(1)
    sp1 = plt.subplot(211)
    sp2 = plt.subplot(212)
    plt.sca(sp1)
    plt.hist(groupMean[values], bins = 50, range = (0,80000))
    plt.sca(sp2)
    plt.hist(groupCount[values], bins = 50, range = (1,10))
    plt.savefig('%s.jpg'%by)
    plt.close('all')
    with open('test.md','a') as file:
        file.write('#### group by %s\n'%by)
        file.write('平均工资和工作岗位最多的前10个%s分别为：\n'%by)
        file.write('|%s|%s|%s|count|\n'%(by, values, by))
        file.write('|----|----|----|----|\n')
        tmp = groupMean.salary.head(10)
        ind = tmp.index
        tmpCount = groupCount.salary.head(10)
        indCount = tmpCount.index
        for i in range(10):
            file.write('|%s|%s|%s|%s|\n'%(ind[i], tmp[i], indCount[i], tmpCount[i]))
        file.write('整体的分布密度图如下: \n')
        file.write('![%s](./%s.jpg)\n'%(by,by))
    return((groupMean, groupCount))


quan = map(lambda x: x/100.0, range(100))

# for beijing
name = ['job', 'company', 'location', 'salary', 'update', 'link']
jobs = pd.read_csv('./jobs2.txt', sep=',sep', names = name)
jobs.salary = list(map(cal, jobs.salary))
unijobs = refine(jobs)
with open('test.md', 'w') as file:
    file.write('### 北京\n')
_,_ = groupStat(unijobs, 'company')
_,_ = groupStat(unijobs, 'job')
print(unijobs.describe())
bj_quant = unijobs.quantile(quan)


# for shanghai
name = ['job', 'company', 'location', 'salary', 'update', 'link']
jobs = pd.read_csv('./jobs.txt', sep=',sep', names = name)
jobs.salary = list(map(cal, jobs.salary))
unijobs = refine(jobs)
with open('test.md', 'a') as file:
    file.write('### 上海\n')
_,_ = groupStat(unijobs, 'company')
_,_ = groupStat(unijobs, 'job')
print(unijobs.describe())
sh_quant = unijobs.quantile(quan)

# for hangzhou
name = ['job', 'company', 'location', 'salary', 'update', 'link']
jobs = pd.read_csv('./jobs3.txt', sep=',sep', names = name)
jobs.salary = list(map(cal, jobs.salary))
unijobs = refine(jobs)
with open('test.md', 'a') as file:
    file.write('### 杭州\n')
_,_ = groupStat(unijobs, 'company')
_,_ = groupStat(unijobs, 'job')
print(unijobs.describe())
hz_quant = unijobs.quantile(quan)

# compare those three cities above
plt.figure()
sp1 = plt.subplot(211)
plt.sca(sp1)
plt.plot(range(100),bj_quant,'',label = 'beijing')
plt.plot(range(100),sh_quant,'',label = 'shanghai')
plt.plot(range(100),hz_quant,'',label = 'hangzhou')
plt.legend(loc = 'upper left')
plt.title("Data Mining Salary")
plt.ylabel("Salary Yuan/month")
sp2 = plt.subplot(212)
plt.sca(sp2)
plt.plot(range(100), bj_quant - sh_quant, label = 'beijing - shanghai')
plt.plot(range(100), hz_quant - sh_quant, label = 'hangzhou - shanghai')
plt.legend(loc = 'upper left')
plt.xlabel("quantile %")
plt.savefig('example.jpg')
with open('test.md', 'a') as file:
    file.write('### 北京、上海、杭州对比\n')
    file.write('三个城市不同分位数水平下的工资对比图如下：\n')
    file.write('![example](./example.jpg)')
