import pandas as pd
import datetime
"""
df=pd.DataFrame(columns={'market','mount','time_open','time_close','cost_open','cost_close','profit'})
df.loc[len(df)]={'market':'BTC-OMG','mount':12,'time_open':'12:30:40','time_close':'none','cost_open':2,'cost_close':'none','profit':0}
df.loc[len(df)]={'market':'BTC-XTC','mount':15,'time_open':'12:30:45','time_close':'12:30:50','cost_open':2,'cost_close':3,'profit':12}

df.to_csv('out.csv')   
df_load=pd.read_csv('out.csv')
df_load.to_csv('out.csv')
df_load=pd.read_csv('out.csv')
update=df_load[['market','mount','profit']][df_load['profit']==0]
"""
#df=pd.read_csv('trade_history.csv')[['market','mount','time_buy','time_sell','cost_buy','cost_sell','profit']]
#df.to_csv('out.csv')
#df=pd.DataFrame(columns={'market','mount','time_buy','time_sell','cost_buy','cost_sell','profit'})
#df.loc[len(df)]={'market':'BTC-OMG','mount':12,'time_buy':'12:30:34','time_sell':'None','cost_buy':0.12,'cost_sell':'None','profit':0}
#df.to_csv('trade_history.csv')
#index_list=df.index[df['market']=='BTC-OMG'][df['cost_sell']==0].tolist()
#cost_buy=df.loc[0]['cost_buy']
#df.set_value(0,'time_sell','12:00:00')
#print (df)
#print (100*0.125/0.123-100)
class trade_history():
    df=[]
    def __init__(self):
        self.df=pd.read_csv('trade_history.csv')[['market','mount','time_buy','time_sell','cost_buy','cost_sell','profit']]
        print ('Load data from trade_history.csv')
    def buy_event(self,market,mount,cost_buy):
        index_list=self.df.index[self.df['market']==market][self.df['time_sell']=='None'].tolist()
        if len(index_list)==0:
            time_buy=datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            self.df.loc[len(self.df)]={'market':market,'mount':mount,'time_buy':time_buy,'time_sell':'None','cost_buy':cost_buy,'cost_sell':'None','profit':0.0}
            self.df.to_csv('trade_history.csv')
            print ('update infor buy ',market,' success')
        else:
            print ('Trade in ',market,' is exit. wait for close trade !')
    def sell_event(self,market,cost_sell):
        index_list=self.df.index[self.df['market']==market][self.df['time_sell']=='None'].tolist()
        print (index_list)
        if len(index_list)==1:
            index=index_list[0]
            cost_buy=self.df.loc[index]['cost_buy']
            time_sell=datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')            
            self.df.set_value(index,'time_sell',time_sell)
            self.df.set_value(index,'cost_sell',cost_sell)
            profit=(100*cost_sell)/cost_buy-100
            self.df.set_value(index,'profit',profit)
            self.df.to_csv('trade_history.csv')
            print ('update infor sell ',market,' success')
        else:
            print ('Trade in ',market,' dont exit.wait for buy coin')
         
#csv=trade_history()
#csv.buy_event('BTC-OMG',10,0.123)
#csv.sell_event('BTC-OMG',0.125)
#df=csv.df          

  
            
            
            
            
        

   