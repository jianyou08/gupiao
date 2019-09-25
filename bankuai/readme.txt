
板块数据：
{
    bankuai_id,   //板块id
    bankuai_name,   //板块id
    [
        {
            gupiao_code,    //板块id
            score,          //股票在该板块的分值
            update_date     //分值更新时间
        },
        ...
    ]
}

板块指数数据：
{
    板块id
    板块名字
    日期
    板块涨跌幅
}

股票数据：
{
    gupiao_code,    //股票代码
    gupiao_name,    //股票名称
    gupiao_xxx,     //市值
    gupiao_cun,     //流通股
}
            
股票价格数据：
股票代码    收盘涨跌幅  收盘价格    开盘价格    5日均线     10日均线    30日均线        股票日期


板块咨询：


股票咨询：
流水id  股票id  咨询类型    内容    利好类型（列好，中，差，无关）