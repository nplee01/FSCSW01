# Strategies to combine indicators
import pandas as pd

from btengine.indicators import IND_MAP

# 3.1 Single indicator
def single(df0, id_list):
    '''
    simple single indictor strategy 
    input: stock price and [indicator and indicator parameters]
    example:
    id_list=[['XMA',50,100]]
    id_cd=id_list[0][0]='XMA'
    id_list1 = id_list[0][1:]=[50,100]
    output: signal depending on the type of selected indicator
    example:
    signal = single(stock,[['BUYNHOLD']])    
    signal = single(stock,[['SMA',200]])        
    signal = single(stock,[['XMA',50,100]]) 
    signal = single(stock,[['XMA',50,100]]) 
    signal = single(stock,[['RSIOBOS',14, 80, 50, 20]])
    signal[:5]
    ''' 
    
    id_cd=id_list[0][0]
    apply_id_type=IND_MAP.get(id_cd)
    id_list1 = id_list[0][1:]
    df = apply_id_type(df0,id_list1)
    
    return df

# 3.2 Multiple indicators using based on same direction
def confluence(df0, id_list):
    '''
    multiple indictors strategy to enter position where all indicators must agreed 
    input: stock price and list of [indicator and indicator parameters]
    example:
    [['SMA',200],['XMA',50,100]]
    output: signal depending on the type of selected indicators
    example:
    signal = confluence(stock,[['SMA',200],['XMA',50,100]])
    signal[:5]
    ''' 
    
    slist =[]
    # currently only handle 2 indicators - for more than 2 indicators consider rewrite this
    # algorithm to recursive
    
    for i, il in enumerate(id_list):
#         print(f'{i} and {il}')
        s=single(df0,[il])
        pos_no='Pos'+str(i)
        s.rename(columns = {'Pos':pos_no},inplace = True)
        slist.append(s)
    
    s3=pd.merge(slist[0],slist[1], right_index=True, left_index=True, how="inner",suffixes=("","_1"))
    s3.loc[(s3.Pos0==s3.Pos1),"Pos"]=s3.Pos0 # Both must agreed    
    s3["Pos"].fillna(0, inplace=True)
    cols=["Open_1","High_1","Low_1","Close_1","Adj Close_1","Volume_1","Pos0","Pos1"]
    s3.drop(cols,axis=1,inplace=True)
    
    return s3

STG_MAP = {
        'SINGLE': single,
        'CONFLUENCE': confluence
}

def apply_strategy(df0, stg_cd, id_list):
    '''
    apply different strategy using different indicators 
    input: stock price, strategy code and list of [indicator and indicator parameters]
    example:
    [['SMA',200],['XMA',50,100]]
    output: signal depending on the type of selected strategy and indicators
    example:
    signal = apply_strategy(stock,'SINGLE',[['BUYNHOLD']])    
    signal = apply_strategy(stock,'SINGLE',[['SMA',200]])        
    signal = apply_strategy(stock,'SINGLE',[['XMA',50,100]]) 
    signal = apply_strategy(stock,'SINGLE',[['RSIOBOS',14, 80, 50, 20]])
    signal = apply_strategy(stock,'CONFLUENCE',[['SMA',200],['XMA',50,100]]) 
    signal = apply_strategy(stock,'CONFLUENCE',[['XMA',50,100],['RSIOBOS',14, 70, 50, 30]])
    signal[:5]
    ''' 
    
    strategy = STG_MAP.get(stg_cd)
    # print(f'{stg_cd} run {strategy}')
    df = strategy(df0,id_list)

    return df
