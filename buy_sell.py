from bittrex import Bittrex
from trade_history import trade_history as trade_h
import threading
import time
import requests
import json
import pandas as pd
import pandas as pd#XMY,VTR,MUE,MEME,KORE,EBST,BTA,BRK,AEON
from stockstats import StockDataFrame as Sdf #DAR,DRACO,GBG,OMNI,PKB,TRUST,PDC
key='1f71e957110745fe9924a5bf19dda49c'
secret='e2e4e16ce88a4b649b5157ea900bf219'
api=Bittrex(key,secret)
def bit_to_usd():
    data=api.get_ticker('USDT-BTC')
    return data['result']['Last']
def exchange_atb(coin):
    market='BTC-'+coin
    data=api.get_ticker(market)
    return data['result']['Ask']
def totalBitcoin():
    data_raw=api.get_balances()
    df=pd.DataFrame(data_raw['result'])
    total=0
    list_btc_value=[]
    for i in range(len(df)):
        if df['Currency'][i]=='BTC':
            value=df['Balance'][i]
        else:
            value=exchange_atb(df['Currency'][i])*df['Balance'][i]   
        total+=value
        list_btc_value.append(value)
    df['BTC_VALUE']=list_btc_value    
    df=df[['Currency','Balance','BTC_VALUE']][df['Balance']>1e-08]      
    df['percent']=df['BTC_VALUE']/df['BTC_VALUE'].sum()*100
    #df['percent']=
    return total,df
def get_bid_ask(market):
    data=api.get_ticker(market)
    return (data['result']['Bid'],data['result']['Ask'])
def sell_buy_immi(type_order,market,mount):    
    (bid,ask)=get_bid_ask(market)
    if type_order=='buy':
       data=api.buy_limit(market,mount,ask)
    else:             
       data=api.sell_limit(market,mount,bid)
    uid=data['result']['uuid']
    time.sleep(1)
    order=api.get_order(uid)
    print (order)
    if order['result']['Closed']!= None:
       print ('exchange is success')                     
    else :  
       print ('exchange is fail')
       api.cancel(uid)
       time.sleep(1)
       sell_buy_immi(type_order,market,mount)
def sell_immi(market,mount):
    sell_success=False
    (bid,ask)=get_bid_ask(market)
    data_get=api.get_balance(market.split('-')[1])
    balance_old=data_get['result']['Balance']
    mount_old=mount
    balance=balance_old    
    while (balance+mount_old) > balance_old:
        data=api.sell_limit(market,mount,bid)
        if data['result']==None:
            print ('Not enough coin to sell or mount is small')
            sell_success=False
            break
        else:
            uid=data['result']['uuid']
            time.sleep(1)
            order=api.get_order(uid)
            if order['result']['Closed']!=None:
                print ('Sell is success')
                sell_success=True
            else:
                print ('Sell is fail')
                api.cancel(uid)
                time.sleep(1)
                
            data_get=api.get_balance(market.split('-')[1])
            balance=data_get['result']['Balance']
            mount=mount_old-(balance_old-balance)
            (bid,ask)=get_bid_ask(market)
    return (sell_success,bid)        
def buy_immi(market,mount):
    buy_success=False
    (bid,ask)=get_bid_ask(market)
    data_get=api.get_balance(market.split('-')[1])
    balance_old=data_get['result']['Balance']
    mount_old=mount
    balance=balance_old    
    while balance*1.006 < balance_old+mount_old:
        data=api.buy_limit(market,mount,ask)
        if data['result']==None:
            print ('Not enough bitcoin to buy or mount is small ')
            buy_success=False
            break
        else:
            uid=data['result']['uuid']
            time.sleep(1)
            order=api.get_order(uid)
            if order['result']['Closed']!=None:
                print ('Buy is success')
                buy_success=True
            else:
                print ('Buy is fail')
                api.cancel(uid)
                time.sleep(1)
                
            data_get=api.get_balance(market.split('-')[1])
            balance=data_get['result']['Balance']
            mount=mount_old-(balance-balance_old)
            (bid,ask)=get_bid_ask(market)            
    return (buy_success,ask)
def percent_total_to_coin(coin,percent):
    total=totalBitcoin()
    mount=percent*total/100
    bit_current=api.get_balance('BTC')['result']['Balance']
    if mount >= bit_current:        
       mount=bit_current
    (bid,ask)=get_bid_ask('BTC-'+coin)
    return mount/ask
def percent_btc(percent):
    balance=api.get_balance('BTC')
    balance=balance['result']['Balance']
    return balance*percent/100
def percent_coin(coin,percent):
    balance=api.get_balance(coin)
    balance=balance['result']['Balance']
    return balance*percent/100
def percent_btc_to_coin(coin,percent):
    balance=api.get_balance('BTC')
    balance=balance['result']['Balance']
    mount_coin_of_percent=balance*percent/100    
    (bid,ask)=get_bid_ask('BTC-'+coin)
    return mount_coin_of_percent/ask
def buy_by_percent(market,percent):
    mount=percent_btc_to_coin(market.split('-')[1],percent)
    buy_immi(market,mount)
def buy_by_total_to_coin(market,percent):
    mount=percent_total_to_coin(market.split('-')[1],percent)
    (result,cost_buy)=buy_immi(market,mount)
    #if result ==True:
        #trade_h.buy_event(market,mount,cost_buy)
        
def sell_buy_percent(market,percent):
    mount=percent_coin(market.split('-')[1],percent)
    (result,cost_sell)=sell_immi(market,mount)
    if result==True:
        trade_h.sell_event(market,cost_sell)

#total,df=totalBitcoin()
#buy_by_total_to_coin('BTC-OMG',15)
#buy_immi('BTC-OMG',0.4)
#sell_immi('BTC-OMG',0.4)
#buy_by_percent('BTC-OMG',10)
#sell_buy_percent('BTC-OMG',100)   
#sell_buy_immi('buy','BTC-OMG',0.5)    
#total=totalBitcoin()
#dolar=total*bit_to_usd()  
#df=totalBitcoin()    
#data=api.get_balance('OMG')
#data=api.get_balances()
#data=api.sell_limit('BTC-OMG',1,0.00141367)
#data=api.buy_limit('BTC-OMG',1,0.00141334)
#uid='3e32fc1f-60d6-4825-ad83-53ca117f41d2'
#data=api.cancel(uid)
#data=api.get_open_orders()
#uid=
#uid='d57e269c-27a3-4167-938c-d8d3aee2b158'
#data=api.get_order(uid)
#data=api.get_marketsummary('BTC-OMG')
#ask=data['result'][0]['Ask']
#lich su tat ca giao dich mua ban
#data=api.get_order_history() 
#(bid,ask)=get_bid_ask('BTC-OMG')
#data=api.sell_limit('BTC-OMG',0.5,bid*1.2)
#data=api.buy_limit('BTC-OMG',0.5,bid*0.8)
#data=api.get_order('ddfdd')
#uid='2a1215db-72c5-49f4-af90-50ba895592fd'
#uid='47f94e52-b64c-4cd6-abea-e44d69e62fb7'
#data=api.get_order(uid)
#data=api.cancel(uid)
 

