# Evaluate performance of strategy used
import pandas as pd

# 6.1 Preprocessing the trading logs
def eval_by_trade(TL0):
    '''
    Preprocessing the trading logs
    Compute equity for each transaction record
    Compute profit and lost per transaction by changed of equity
    Compute cummulative profit and lost
    input: transaction log dataframe
    output: new transaction log with equity, P&L and cummulative P&L
    example:
    print(TL.PL.sum())
    TL1 = eval_by_trade(TL)
    TL1
    '''
    
    TL = TL0.copy()
    
    TL.loc[TL.trxType=='Enter Long',"trxUnit"] = TL.trxUnit
    TL.loc[TL.trxType=='Exit Long',"trxUnit"] = -1*TL.trxUnit
    TL.loc[TL.trxType=='Enter Long',"trxVal"] = -1*TL.trxVal
    TL.loc[TL.trxType=='Exit Long',"trxVal"] = TL.trxVal
    TL["trxEquity"]=TL.trxPrice*TL.trxUnitBal+TL.trxCashBal
    TL["PL"]=TL.trxEquity-TL.trxEquity.shift(1)
    TL["CumPL"]=TL.PL.cumsum()
    
    return TL

# 6.2 Group Trx Enter/Exit to trxGroupNo

def gen_trade_no (TL0):
    '''
    To generate trade number by pairing enter and exit a transaction
    input: trading log
    output: trading log with trade number
    example:
    TL1 = gen_trade_no (TL1)
    TL1[["trxType","trxGroupNo"]]
    '''

    TL = TL0.copy()
    
    tp = len (TL)
    tl2 = []

    trxGroupNo = 0
    cPos = 0
    for i in range(tp):
        if (TL.trxType[i] == 'Enter Long'):
            cPos = 1
            tl2 = tl2 + [[TL.index[i].date(),trxGroupNo]]
        elif (TL.trxType[i] == 'Exit Long' and cPos==1):       
            cPos = 0
            tl2 = tl2 + [[TL.index[i].date(),trxGroupNo]]
            trxGroupNo = trxGroupNo + 1
   
    TL2 =pd.DataFrame(tl2, columns =['trxDate','trxGroupNo'])
    datetime_series = pd.to_datetime(TL2['trxDate'])
    # create datetime index passing the datetime series
    datetime_index = pd.DatetimeIndex(datetime_series.values)
    TL2=TL2.set_index(datetime_index)
    TL2.drop('trxDate',axis=1,inplace=True)
    # 5.3 Merge TL and TL2
    TL3 = pd.merge(TL0,TL2, left_index=True, right_index=True,how='inner')
    return TL3

# 6.3 Analyze Profit and Lost    

def gen_PL_stat(TL, verbose=False):
    '''
    Using closed trades to compute and store the trading statistics based on profit and lost
    input: trading log with P&L and trade number
    output: P&L statistics in dictionary format
    example:
    PL_stat=gen_PL_stat(TL1,verbose=False)
    TL1.describe()
    PL_stat
    '''

    CT=TL[TL.trxType=="Exit Long"]
    PT=CT[CT.PL > 0]
    LT=CT[CT.PL < 0]
    
    #Create a dictionary to store the results
    trade_stat = {}
    sCT=CT.describe()
    sPT=PT.describe()
    sLT=LT.describe()
    sCT=sCT.fillna(0)
    sPT=sPT.fillna(0)
    sLT=sLT.fillna(0)
    trade_stat.update(
        {'overallTrade':
         {'count': len(CT),
          'trxPrice': {'mean':sCT.loc["mean","trxPrice"],
                       'min':sCT.loc["min","trxPrice"],
                       'max':sCT.loc["max","trxPrice"],
                       'std':sCT.loc["std","trxPrice"]
                      },
          'trxEquity': {'mean':sCT.loc["mean","trxEquity"],
                       'min':sCT.loc["min","trxEquity"],
                       'max':sCT.loc["max","trxEquity"],
                       'std':sCT.loc["std","trxEquity"]
                      }, 
          'PL': {'mean':sCT.loc["mean","PL"],
                       'min':sCT.loc["min","PL"],
                       'max':sCT.loc["max","PL"],
                       'std':sCT.loc["std","PL"]
                      } 
         },
         'profitTrade':
         {'count': len(PT),
          'trxPrice': {'mean':sPT.loc["mean","trxPrice"],
                       'min':sPT.loc["min","trxPrice"],
                       'max':sPT.loc["max","trxPrice"],
                       'std':sPT.loc["std","trxPrice"]
                      },
          'trxEquity': {'mean':sPT.loc["mean","trxEquity"],
                       'min':sPT.loc["min","trxEquity"],
                       'max':sPT.loc["max","trxEquity"],
                       'std':sPT.loc["std","trxEquity"]
                      }, 
          'PL': {'mean':sPT.loc["mean","PL"],
                       'min':sPT.loc["min","PL"],
                       'max':sPT.loc["max","PL"],
                       'std':sPT.loc["std","PL"]
                      } 
         },
         'lossingTrade':
         {'count': len(LT),
          'trxPrice': {'mean':sLT.loc["mean","trxPrice"],
                       'min':sLT.loc["min","trxPrice"],
                       'max':sLT.loc["max","trxPrice"],
                       'std':sLT.loc["std","trxPrice"]
                      },
          'trxEquity': {'mean':sLT.loc["mean","trxEquity"],
                       'min':sLT.loc["min","trxEquity"],
                       'max':sLT.loc["max","trxEquity"],
                       'std':sLT.loc["std","trxEquity"]
                      }, 
          'PL': {'mean':sLT.loc["mean","PL"],
                       'min':sLT.loc["min","PL"],
                       'max':sLT.loc["max","PL"],
                       'std':sLT.loc["std","PL"]
                      } 
         }
        }
    )
    
    if verbose:
        print(f'Completed trades: Profitable {len(PT)}, Loss making {len(LT)}')
        print('Profit statistics\n', PT.describe())
        print('Lost statistics\n',LT.describe())
        print('-'*70)

    #Find best trade
    if (len(PT)>0):
        best_tradeValue = PT.PL.max()
        best_tradeClosingDate=PT.PL.idxmax().strftime("%Y-%m-%d") 
        trxGroupNo=TL.loc[best_tradeClosingDate].trxGroupNo
        best_tradeEnterDate=TL[(TL.trxType=='Enter Long') & (TL.trxGroupNo==trxGroupNo)].index.astype(str)
        trade_stat.update(
            {'bestTrade':
                {'trxGroupNo':trxGroupNo,'enter': best_tradeEnterDate[0], 'exit':best_tradeClosingDate, 'amount':best_tradeValue}
            })
        
        if verbose:
            print (f'Best trade enter date on {best_tradeEnterDate[0]} closing on {best_tradeClosingDate} making a profit of {best_tradeValue:.2f}')

    #Find worst trade
    if (len(LT)>0):
        worst_tradeValue = LT.PL.min()
        worst_tradeClosingDate=LT.PL.idxmin().strftime("%Y-%m-%d")
        trxGroupNo=TL.loc[worst_tradeClosingDate].trxGroupNo
        worst_tradeEnterDate=TL[(TL.trxType=='Enter Long') & (TL.trxGroupNo==trxGroupNo)].index.astype(str)
        trade_stat.update(
                {'worstTrade':
                    {'trxGroupNo':trxGroupNo,'enter': worst_tradeEnterDate[0], 'exit':worst_tradeClosingDate, 'amount':worst_tradeValue}
                })
        if verbose:
            print(f'Worst trade enter date on {worst_tradeEnterDate[0]} closing on {worst_tradeClosingDate} making a lost of {worst_tradeValue:.2f}')
            
    
    return trade_stat

# 6.4 Daily Equity Valuation

def daily_val(S0, TL0):
    '''
    To perform daily evaluation of equity position so that we can compute:
    daily P&L, daily cummulative P&L and daily drawdown
    Important program to verify trading results
    input: signal and trading log with P&L dataframe
    output: daily valuation dataframe
    example:
    TL1 = eval_by_trade(TL)
    TL1 = gen_trade_no(TL1)
    PL_stat=gen_PL_stat(TL1)
    DV = daily_val(signal, TL1)
    DV.info()
    DV.to_excel("testDV3.xls")
    '''
    
    dv = pd.merge(S0,TL0,left_index=True, right_index=True,how='left')
    dv.drop(['Adj Close'], axis=1,inplace=True)
    #dv[pd.notnull(dv["PL"])]
    dv["PL"].fillna(0, inplace = True)
    startCapital=TL0.StartCapital[0]
    dv["StartCapital"].fillna(startCapital, inplace=True)
    cols=["trxPrice","trxUnit","trxCost","trxVal","trxCashBal","trxUnit","trxUnitBal"]
    dv[cols]=dv[cols].fillna(0)
    dv.loc[str(dv.index.values[0].astype(str)),"trxVal"]=startCapital
    dv["dailyCumPL"]=dv.PL.cumsum()
    dv["dailyCashBal"]=dv.trxVal.cumsum()
    dv["dailyUnitBal"]=dv.trxUnit.cumsum()
    # Mark to Market - Chage from Opening Price to Close price
    dv["dailyVShare"]=dv.Close*dv.dailyUnitBal
    # Calculate Equity Value
    dv["dailyEquity"]=dv.dailyVShare+dv.dailyCashBal
    dv["dailyEquityPL"]=dv.dailyEquity-dv.dailyEquity.shift(1)
    # Calculate Drawdown    
    dv["dailyEquityCumPL"]=dv.dailyEquityPL.cumsum()
    dv["dailyCumPLmax"] = dv.dailyCumPL.cummax()
    dv["dailyDrawdown"] = dv.dailyCumPLmax - dv.dailyCumPL
    
    return dv

# 6.5 Gen and Print Back Testing Statistics
def gen_bt_stat (BTStrategy, stock_name, initCapital, DV, PL_stat, stg_cd, id_list, print_stat=True):
    '''
    Generate back testing statistics from daily evaluation and P&L statistics dataframe
    input: BT strategy, stock name, init capital, daily valuation, P&L statistics, 
    strategy name, strategy code, indicators list with their respective param
    output: backtesting performance results in dictionary format
    
    example:
     DV = daily_val(signal, TL1)
     bt_stat=gen_stat (BT_strategy, stock_name, init_capital, DV, PL_stat, stg_cd, id_list, print_stat=True)
     with open("123P.json", "w") as outfile:
          json.dump(bt_stat, outfile)
     DV.to_excel(str(run_no)+"G.xls")
    '''
    
    bt_pf ={}
    bt_pf['StockName']=stock_name
    bt_pf['InitCapital']=initCapital
    bt_pf['FinalEquity']=DV.dailyEquity[-1]
    bt_pf['CurrentShareMarketValue']=DV.dailyVShare[-1]
    bt_pf['CurrentCashBalance']=DV.dailyCashBal[-1]
    bt_pf['EquityPerfomance']=bt_pf['FinalEquity']- bt_pf['InitCapital']
    if (print_stat):
        print(f"{BTStrategy} on {bt_pf['StockName']} Initial Capital:{bt_pf['InitCapital']:.2f}, Final Equity Value: {bt_pf['FinalEquity']:.2f}")
        print(f"Final Equity consist of Current Share Market Value: {bt_pf['CurrentShareMarketValue']:.2f} and Cash Balance: {bt_pf['CurrentCashBalance']:.2f}")
        print(f"Equity performace is {bt_pf['EquityPerfomance']:.2f}")
    if initCapital > 0:
        bt_pf['EquityROI']=bt_pf['EquityPerfomance']/bt_pf['InitCapital']*100
        if (print_stat):
            print(f"Equity ROI is {bt_pf['EquityROI']:.2f}%")
    bt_pf['TradeCount'] = PL_stat['overallTrade']['count']
    bt_pf['ProfitTradeCount'] = PL_stat['profitTrade']['count']
    bt_pf['LossingTradeCount'] = PL_stat['lossingTrade']['count']
    if (print_stat):
            print(f"Number of trade: {bt_pf['TradeCount']} profitable: {bt_pf['ProfitTradeCount']} lossing: {bt_pf['LossingTradeCount']}")               
    if bt_pf['TradeCount'] > 0:
        bt_pf['WinRate']=bt_pf['ProfitTradeCount']/bt_pf['TradeCount']*100
        bt_pf['MaxDrawdownValue']=DV.dailyDrawdown.max()
        bt_pf['MaxDrawdownDate']=DV.dailyDrawdown.idxmax().strftime("%d-%m-%Y")
        if (print_stat):
            print(f"Win rate: {bt_pf['WinRate']:.2f}%")
            print(f"Max drawdown {bt_pf['MaxDrawdownValue']:.2f} on {bt_pf['MaxDrawdownDate']}")
    
    # Add in the strategies and the indicators used along with their params
    # Indicators used to be display on the test history page
    indicators_str = ''
    for ind in id_list:
        indicators_str += f'{indicator_dict.get(ind[0])} ' + str([i for i in ind[1:]]) + ', '

    # Remove the last ', '
    indicators_str = indicators_str[:-2]

    # Replacing the [ ] to ( )
    indicators_str = indicators_str.replace('[', '(').replace(']', ')')

    # Insert the indicators used into the json
    bt_pf['StrategyCode']=stg_cd # Either SINGLE or CONFLUENCE

    # Replacing the XMA and RSIOBOS 
    bt_pf['StrategyIndicators']=indicators_str # Example: SMA Baseline (200)

    # Indicators list: custom output for different indicators used
    # NOTE: To be converted into a function that take from a indicators dict
    for ind in id_list:
        if ind[0] == 'SMA':
            bt_pf['SMA'] = ind[1] # Eg: 200
        elif ind[0] == 'XMA':
            bt_pf['SMA_F'] = ind[1] # Eg: 50
            bt_pf['SMA_S'] = ind[2] # Eg: 100
        elif ind[0] == 'RSIOBOS':
            bt_pf['RSIOBOS_PERIOD'] = ind[1]
            bt_pf['RSIOB'] = ind[2]
            bt_pf['RSI_BASE'] = ind[3]
            bt_pf['RSIOS'] = ind[4]

    return bt_pf

indicator_dict = {
    'SMA': "SMA Baseline",
    'XMA': "SMA Crossing",
    'RSIOBOS': "RSI OB/OS",
}