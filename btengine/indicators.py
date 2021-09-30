# Indicators to generate trading signals from price data
import talib as ta

# 2.0 Special case for benchmark only - Buy and hold 
def apply_id_buy_and_hold(df0,plist):
    '''
    apply buy and hold strategy as benchmark for backtesting
    input: stock price and null parameter list
    output: stock price with long position
    example:
    signal = apply_id_buy_and_hold(stock,[])
    print(apply_id_buy_and_hold.__doc__)
    signal[:5]
    '''
    
    df=df0.copy()

    df["Pos"]=1 # Long and hold
    return df

# 2.1 Single SMA indicator as baseline
def apply_id_sma_baseline(df0,plist):
    '''
    apply sma as a baseline for backtesting
    input: stock price and parameter list with first element is the timeperiod
    output: stock price with long position if above baseline, short position if below baseline
    example:
    sma_b=200
    signal=apply_id_sma_baseline(stock,[sma_b])
    signal[signal.SMA.notnull()]
    signal[:5]
    '''      
    sma_b=plist[0]
    df = df0.copy()
    df["SMA"] = ta.SMA(df.Close, timeperiod=sma_b)
    df.dropna(inplace = True)
    df.loc[(df.Close > df.SMA),"Pos"] = 1 # Long Position
    df.loc[(df.Close <= df.SMA),"Pos"] = -1 # Short Position
    return df

# 2.2 SMA Crossing
def apply_id_sma_crossing(df0,plist):
    '''
    apply sma crossing for backtesting
    input: stock price and parameter list with 2 timeperiods, fast and slow sma
    output: stock price with long position if fast above slow, vice versa
    example:
    sma_f=50
    sma_s=100
    signal=apply_id_sma_crossing(stock,[sma_f,sma_s])
    signal[:5]
    ''' 
    
    sma_f=plist[0]
    sma_s=plist[1]
    df = df0.copy()
    df["SMA_F"] = ta.SMA(df.Close, timeperiod=sma_f)
    df["SMA_S"] = ta.SMA(df.Close, timeperiod=sma_s)
    df.dropna(inplace = True)
    df.loc[(df.SMA_F > df.SMA_S),'Pos'] = 1 # Long Position
    df.loc[(df.SMA_F <= df.SMA_S),'Pos'] = -1 # Short Position
    
    return df

# 2.3 RSI over bought and over sold
def apply_id_rsi_obos(df0,plist):
    '''
    apply rsi indicator to detect overbought or oversold conditions
    input: stock price and parameter list with 4 elements:  timeperiod, overbought, baseline, oversold
    output: stock price with long position if oversold and short if overbought, otherwise do nothing
    example:
    rsi_tp=14
    rsi_ob=80
    rsi_bl=50
    rsi_os=20
    signal=apply_id_RSI_OBOS(stock,[rsi_tp, rsi_ob, rsi_bl, rsi_os])
    signal[:5]
    ''' 
        
    rsi_tp=plist[0]
    rsi_ob=plist[1]
    rsi_bl=plist[2]
    rsi_os=plist[3]
    df = df0.copy()
    df["RSI"] = ta.RSI(df.Close, timeperiod=rsi_tp)
    df.dropna(inplace = True)
    df['Pos'] = 0
    df.loc[(df.RSI > rsi_ob),'Pos'] = -1 # Short Position
    df.loc[(df.RSI <= rsi_os),'Pos'] = 1 # Long Position
    
    return df

# 2.10 Map the apply indicator funtions to a dictionary
IND_MAP = {
        'BUYNHOLD': apply_id_buy_and_hold,
        'SMA': apply_id_sma_baseline,
        'XMA': apply_id_sma_crossing,
        'RSIOBOS': apply_id_rsi_obos}
