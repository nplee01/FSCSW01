from datetime import date
from api import api_bt_run
# Testing. PYTHONPATH must have project home.
if __name__ == '__main__':

    # status=api_bt_run(123, 'TENAGA',date(2000,1,1),date(2021,10,31),10000,1000,'Buy and Hold','SINGLE',
    # [['BUYNHOLD']], True)
    # status=api_bt_run(123, 'TENAGA',date(2000,1,1),date(2021,10,31),10000,1000,'SMA as Baseline',
    # 'SINGLE',[['SMA',200]], True)
    # status=api_bt_run(123, 'TENAGA', date(2000,1,1),date(2021,10,31),10000,1000,'SMA Crossing','SINGLE',
    #         [['XMA',50,100]], True)
    # status=api_bt_run(123, 'TENAGA',date(2000,1,1),date(2021,10,31),10000,1000,'RSI OB/OS','SINGLE',
    #     [['RSIOBOS',14, 80, 50, 20]], True)
    status=api_bt_run(123, 'TENAGA',date(2000,1,1),date(2021,10,31),10000,1000,
        'Confluence SMA Crossing and SMA Baseline','CONFLUENCE',[['SMA',200],['XMA',50,100]], True)

    if status:
        print ('success')
    else:
        print('no data')
