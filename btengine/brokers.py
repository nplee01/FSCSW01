# Broker module to handle orders and trades
import pandas as pd

def generate_order(df0):
    '''
    generate orders to broker based on signal dataframe
    if today closing signal buy, then buy on next day
    input: signal dataframe
    output: order dataframe
    example:
    signal = apply_id_buy_and_hold(stock,[])
    order = generate_order(signal)
    order.info()
    ''' 
    
    df=df0.copy()

    df["buyOrder"]=0 # Do nothing
    df["shortOrder"]=0 # Do nothing
    
    df["YPos"]=df["Pos"].shift(1)
    df["YPos"].fillna(0, inplace=True)
    # Check day 1 closing price if signal is long position buy tomorrow
    fDate=str(df.index.values[1].astype(str)) #convert numpy_str to string
    if (df.Pos[fDate]==1):
        df.loc[fDate,"buyTomorrow"]=1
    
    df.loc[((df["Pos"]== 0) & (df["YPos"]== -1)),"buyTomorrow"]=-1
    df.loc[((df["Pos"]== 1) & (df["YPos"]== -1)),"buyTomorrow"]= 1
    df.loc[((df["Pos"]== -1) & (df["YPos"]== 1)),"buyTomorrow"]=-1
    df.loc[((df["Pos"]== 0) & (df["YPos"]==1)),"buyTomorrow"]= 1
    
    df["buyOrder"]=df["buyTomorrow"].shift(1) # buy order on Day T+1 at Opening Price
    
    df["buyOrder"].fillna(0, inplace=True)
    order = df[df['buyOrder']!=0]   
    return order

# 5. Simulate broker execute order
   

def record_trade(log0, date0, type0, buyOrder, shortOrder, price, unit, cost, trxVal, cashBal, unitBal, initCapital):
    
    log1=log0+[[date0,type0,buyOrder,shortOrder,price,unit,cost,trxVal,cashBal,unitBal,initCapital]]
    return log1
    
def cost_of_trade(df0, unit):
    return 0


def broker_simulator(order, capital=0, orderSize=1000, allowShort=False, verbose=True):
    '''
    broker buy or sell on open price based on order instruction dataframe
    if today closing signal buy/sell, then buy/sell on next day
    input: order instruction dataframe
    output: trading logs (TL) dataframe for further evaluation
    example:
    signal = apply_id_buy_and_hold(stock,[])
    order = generate_order(signal)
    TL=broker_simulator(order,0)
    or
    TL=broker_simulator(generate_order(apply_id_buy_and_hold(read_stock("TENAGA"))),0)
    TL
    TL.to_excel("testTL.xls")
    ''' 
     
    nshare = 0 #number of share
    vshare = 0 #value of share
    unit = orderSize # transaction unit

    df=order.copy()
    
    tradingLog=[] #Trading Log, structure not good enough to analyze trading performance      
    sp = len(df) #simulation period
    orderType = ""
    cashBal = capital
    unitBal = 0
    longPos = False

    for b in range(sp):
        price=df.Open[b]
        buy_order = df.buyOrder[b]
        short_order = df.shortOrder[b] # for future used
        
        if (buy_order==1)and not(longPos):
            orderType="Enter Long"
            longPos = True
            vshare = price*unit
            cost=cost_of_trade(df,unit)
            trxVal=vshare + cost
            cashBal = cashBal - trxVal
            unitBal = unitBal + unit
            tradingLog=record_trade(tradingLog,df.index[b].date(),orderType,buy_order,short_order,price,unit,cost,trxVal,cashBal,unitBal,capital)                       
            if verbose:
                print(f"{b} on {df.index[b].date()}: {orderType} {unit} unit @ Price: {price:.2f}") 
            
        elif (buy_order==-1): 
            if longPos:
                orderType="Exit Long"
                longPos = False
                nshare = nshare - unit
                vshare = price*unit
                cost=cost_of_trade(df,unit)
                trxVal=vshare - cost
                cashBal = cashBal + trxVal
                unitBal = unitBal - unit
                tradingLog=record_trade(tradingLog,df.index[b].date(),orderType,buy_order,short_order,price,unit,cost,trxVal,cashBal,unitBal,capital)                  
                if verbose:
                    print(f"{b} on {df.index[b].date()}: {orderType} {unit} unit @ Price: {price:.2f}")
                                                              
    df2 =pd.DataFrame(tradingLog, columns =['trxDate','trxType','buyOrder','sellOrder','trxPrice','trxUnit','trxCost','trxVal','trxCashBal','trxUnitBal','StartCapital'])
    datetime_series = pd.to_datetime(df2['trxDate'])
    # create datetime index passing the datetime series
    datetime_index = pd.DatetimeIndex(datetime_series.values)
    df2=df2.set_index(datetime_index)
    df2.drop('trxDate',axis=1,inplace=True)
    
    return df2
