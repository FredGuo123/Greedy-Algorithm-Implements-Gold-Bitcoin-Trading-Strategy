**这个是使用贪心算法实现黄金比特币交易策略的完整代码 **
整个代码是按照黄金和比特币价格的波动进行比较激进的交易，作者以2016年初到19年年底的数据作为测试，以三十天的数据预测未来一天的数据，并且使用这个策略，最终本金1000美金赚到了14亿美金，
这是一个惊人的 结果！ 
思路： 
①首先将黄金和比特币的预测价格整合到同一个表格中，注意黄金市场闭市的时间. 
②我们先从单一的商品运用贪心算法进行规划，分两种情况： 
Ⅰ若今天预测得到明天涨价，则今天买入直至某一天预测到当天的明天跌价则当天卖出。 
Ⅱ若今天预测得到明天跌价，则今天卖出直至某一天预测到当天的明天涨价则当天买入。 
③由单一商品的情况推广到对于黄金和比特币的情况运用贪心算法进行规划，分为六种情况： 
Ⅰ若今天预测二者变化幅度均在α%内，则不交易（其中α%为佣金占有的比例，此时若要交易，得到的利润并不足以支付佣金） 
Ⅱ若今天预测一个变化幅度在α%内，另一个涨幅超过α%，则将所有资产转化为涨幅超过α%的商品 
Ⅲc Ⅳ若今天预测二者变化幅度均超过α%，且均为涨幅，则比较二者扣除α%后的大小，将所有资产转化为选择扣除后涨幅大的商品 
Ⅴ若今天预测二者变化幅度均超过α%，且均为跌幅，则将所有资产转化为货币 
Ⅵ若今天预测二者变化幅度均超过α%，且为一涨一跌，则将所有资产转化为涨价的商品
