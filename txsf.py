import pandas as pd

gold_predict = pd.read_csv('/Users/fredguo/Documents'
                           '/MCM:ICM/2022_Problem_C_DATA/LBMA-GOLD-预测.csv',
                           header=0, encoding='gbk')
gold_data = pd.read_csv('/Users/fredguo/Documents/MCM:ICM'
                        '/2022_Problem_C_DATA/LBMA-GOLD-3.0.csv',
                        header=0)
gold = pd.merge(gold_data, gold_predict, on='Date', how='left')
gold ['Date'] = pd.to_datetime(gold ['Date'], format='%Y/%m/%d')
gold.index = gold['Date']
del gold['Date']
bit_predict = pd.read_csv('/Users/fredguo/Documents/MCM:ICM'
                          '/2022_Problem_C_DATA/BCHAIN-MKPRU-预测.csv',
                          header=0, encoding='gbk')
bit_data = pd.read_csv('/Users/fredguo/Documents/MCM:ICM'
                       '/2022_Problem_C_DATA/BCHAIN-MKPRU-2.0.csv',
                       header=0)
bit = pd.merge(bit_data, bit_predict, on='Date', how='left')
bit['Date'] = pd.to_datetime(bit_data['Date'], format='%Y/%m/%d')
bit.index = bit['Date']
del bit['Date']
all_data = bit.join(gold, how='left')
all_data = all_data.reset_index()
all_data = all_data.fillna(method='pad', axis=0)
all_data = all_data.sort_index(ascending=True)
all_data = all_data.dropna()
all_data['gold growth rate'] = (all_data['gold price']
                                .pct_change())*100
all_data['Bitcoin growth rate'] = (all_data['bitcoin price']
                                   .pct_change())*100
df1 = all_data[['bitcoin price', 'gold price']]
df2 = all_data[['Bitcoin price prediction', 'Gold forecast price']]
df2 = df2.drop(labels=1)
df2 = df2.reset_index()
del df2['index']
#df2 = df2.shift()
#df2 = df2.fillna(0.0)
df1 = df1.reset_index()
del df1['index']
df1 = df1.join(df2, how='left')
df1 = df1.dropna(axis=0,how='any')
df1['Gold forecast growth rate'] = ((df1['Gold forecast price']
                                     - df1['gold price'])
                                    /df1['gold price'])*100
df1['Bitcoin forecast growth rate'] = ((df1['Bitcoin price prediction']
                                        - df1['bitcoin price'])
                                       /df1['bitcoin price'])*100
df1 = df1.shift()
df1 = df1.fillna(0.0)
df3 = df1[['Gold forecast growth rate', 'Bitcoin forecast growth rate']]

all_data = all_data.fillna(0.0)

all_data = all_data.reset_index()
del all_data['index']
all_data = all_data.T
df3 = df3.T
all_data = pd.concat([all_data, df3]).T

Gold = 0.0
Bitcoin = 0.0
Money = 1000.0
a = 1.0 #gold
b = 2.0 #bit

for i in range(1, 1824):
    if all_data.iat[i,5]==0:
        all_data.iat[i,7]=0.0

for i in range(1,1824):
    if all_data.iat[i,7]<=a and all_data.iat[i,7]>=-a \
            and all_data.iat[i,8]<=b \
            and all_data.iat[i,8]>=-b:
        Gold = Gold*(1+(all_data.iat[i,5])*0.01)
        Bitcoin = Bitcoin*(1+(all_data.iat[i,6])*0.01)

    else:
        if all_data.iat[i, 7] <= a \
                and all_data.iat[i, 7] >= -a \
                and all_data.iat[i, 8] >= b:
            Bitcoin = Bitcoin + Gold * (1 - (a + b) * 0.01) \
                      + Money * (1 - b * 0.01)
            Gold = 0
            Money = 0
            Bitcoin = Bitcoin * (1 + (all_data.iat[i, 6]) * 0.01)
        else:
            if all_data.iat[i, 8] <= b \
                    and all_data.iat[i, 8] >= -b \
                    and all_data.iat[i, 7] >= a:
                Gold = Gold + Bitcoin * (1 - (a + b) * 0.01) \
                       + Money * (1 - a * 0.01)
                Bitcoin = 0
                Money = 0
                Gold = Gold * (1 + (all_data.iat[i, 5]) * 0.01)
            else:
                if all_data.iat[i, 7] <= a \
                        and all_data.iat[i, 7] >= -a \
                        and all_data.iat[i, 8] <= -b:
                    Gold = Gold * (1 + (all_data.iat[i, 5]) * 0.01)
                    Money = Money + Bitcoin * (1 - b * 0.01)
                    Bitcoin = 0
                else:
                    if all_data.iat[i, 8] <= b \
                            and all_data.iat[i, 8] >= -b \
                            and all_data.iat[i, 7] <= -a:
                        Bitcoin = Bitcoin * (1 + (all_data.iat[i, 6]) * 0.01)
                        Money = Money + Gold * (1 - a * 0.01)
                        Gold = 0
                    else:
                        if all_data.iat[i, 7] >= a \
                                and all_data.iat[i, 8] >= b:
                            if (all_data.iat[i, 7] - a) > (all_data.iat[i, 8] - b):
                                Gold = Gold + Money \
                                       * (1 - a * 0.01) \
                                       + Bitcoin * (1 - (a + b) * 0.01)
                                Gold = Gold * (1 + (all_data.iat[i, 5]) * 0.01)
                                Money = 0
                                Bitcoin = 0
                            else:
                                Bitcoin = Bitcoin + \
                                          Money * (1 - b * 0.01) \
                                          + Gold \
                                          * (1 - (a + b) * 0.01)
                                Bitcoin = Bitcoin * \
                                          (1 + (all_data.iat[i, 6]) * 0.01)
                                Money = 0
                                Gold = 0
                        else:
                            if all_data.iat[i, 7] <= -a \
                                    and all_data.iat[i, 8] <= -b:
                                Money = Money+Bitcoin \
                                        * (1 - b * 0.01) \
                                        + Gold * (1 - a * 0.01)
                                Gold = 0
                                Bitcoin = 0
                            else:
                                if all_data.iat[i, 7] <= -a \
                                        and all_data.iat[i, 8] >= b:
                                    Bitcoin = Bitcoin + \
                                              Money * (1 - b * 0.01) \
                                              + Gold * (1 - (a + b) * 0.01)
                                    Bitcoin = Bitcoin * \
                                              (1 + (all_data.iat[i, 6]) * 0.01)
                                    Gold = 0
                                    Money = 0
                                else:
                                        Gold = Gold + \
                                               Money * (1 - a * 0.01) \
                                               + Bitcoin * (1 - (a + b) * 0.01)
                                        Gold = Gold * \
                                               (1 + (all_data.iat[i, 5]) * 0.01)
                                        Bitcoin = 0
                                        Money = 0
print('The gold trade cost is:')
print(a)
print('Bitcoin trade cost is:')
print(b)
print('Finally we earned:')
print(Money+Gold+Bitcoin)









