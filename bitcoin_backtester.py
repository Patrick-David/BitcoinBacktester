
"""Bitcoin Backtester that runs a cointegration strategy
and prints out to console the results tick by tick.
This version is designed for being run in the terminal as it
doesn't produce any plotting.
For the more visual version, see the ipynb version
included in this repo

This backtester is defaulted to running BTC and BCH at daily
frequency, but feel free to change the params in the Data_Puller
class instantiation.

to run in terminal - cd into the repo and type 'python bitcoin_backtester.py'
 """


#fetches crypto data, cleans then passes to container df3

#Class to store data for any pairs, crypto or otherwise
class Data_Puller:
    def __init__(self,ticker1,ticker2,freq,periods):
        self.ticker1 = ticker1
        self.ticker2 = ticker2
        self.freq = freq
        self.periods = periods
        self.df3 = pd.DataFrame()
        
        
        
    #method to pull, munge, store crypto pairs data
    def get_data(self):
        #replace this in final merge
        b = 3.995977
        _data1 = requests.get(f"https://min-api.cryptocompare.com/data/histo{self.freq}?fsym={self.ticker1}&tsym=USD&limit={self.periods}").json()['Data']
        _data2 = requests.get(f"https://min-api.cryptocompare.com/data/histo{self.freq}?fsym={self.ticker2}&tsym=USD&limit={self.periods}").json()['Data']
        df1 = pd.DataFrame(_data1)
        df1_close = df1['close']
        df2 = pd.DataFrame(_data2)
        df2_close = df2['close']
        
        df1['time'] = pd.to_datetime(df1['time'],unit='s')
        df1.set_index(df1['time'], inplace = True)
        
        df2['time'] = pd.to_datetime(df2['time'],unit='s')
        df2.set_index(df2['time'], inplace = True)
        df1 = df1.drop(['high','low','open','volumefrom','volumeto','time'] ,axis=1)
        df2 = df2.drop(['high','low','open','volumefrom','volumeto'] ,axis=1)
        df1.rename(columns={'close': 'BTC'}, inplace=True)
        df2.rename(columns={'close': 'BCH'}, inplace=True)
        #print(df1.head())
        #print(df2.head())
        self.df3 = pd.concat([df1,df2],axis=1)
        #self.df3['spread'] = self.df3[self.ticker1] - self.df3[self.ticker2]
        #self.df3['spread_pct_change'] = self.df3['spread'].pct_change()
        #add cointegration model X1 - X2 = should be stationary
        self.df3['full_z_coint'] = self.df3['BTC'] - b*self.df3['BCH']
        self.df3['b_x_bch'] = b*self.df3['BCH']
        
        #prints df to check data
        print(self.df3)
        
    #returns the final dataframe, with 1st element dropped as its nan for spread_pct_change    
    def fetch_df(self):
        return self.df3.loc['2017-12-12':]
        


class Portfolio:
    def __init__(self):
        #self.orders = pd.DataFrame(columns=['TS','Order','tick1','tick2'])
        self._port = pd.DataFrame(columns=['ts','signal','action','sold_value','bought_value','U_pnl','R_pnl'])
#        self.current_budget = 1000000
        self.signal = None
        self.prev = None
        #bought / sold
        self.current_pos= "empty"
        #self.pnl = pd.DataFrame(columns = ['pnl'])
        self.bought_sold_price = 0
        self.stamp = 0
        #self.sold_value = 0
        #self.bot_value = 0
        self.sell_units = 0
        self.buy_units = 0
        self.value_2 = 0
        self.value_1 = 0
        self.rpl = 0
    
    def close_out(self):
        self.rpl += (1000 - self.value_2) + (self.value_1 - 1000)
        self.current_pos ='empty'

        print("close out position")
        
   
        
        
        
        
    def position(self,ts,tick1,tick2,price,tot_trade_amount=2000):
        print()
        print(self.stamp)
        print('current pos:',self.current_pos)
        print("bought / sold price: ",self.bought_sold_price)
        print('this is prev:', self.prev)
        print('this is the signal:',self.signal)
        single_trade_amount = tot_trade_amount/2
        action = None
        
        
        
        if self.signal =="Hold":
            
            if self.current_pos =='sold':
                print("sold tick")
                self.value_2 = self.sell_units * tick2
                self.value_1 = self.buy_units * tick1
            elif self.current_pos == 'bought':
                self.value_2 = self.sell_units * tick1
                self.value_1 = self.buy_units * tick2
            else:
                print("Hold neither bought nor sold")
                self.value_2 = 0
                self.value_1 = 0
                
                
                
          
            print("hold 1")
            print("caputured by Hold")
            
            if self.current_pos == 'bought' and price > self.mu:
                print("hold 2")
                self.close_out()
                action = "Closed out Long"
                #self.current_pos ='empty'
                
            elif self.current_pos =='sold' and price < self.mu:
                print("hold 3")
                self.close_out()
                action = "Closed out Short"
                #self.current_pos ='empty'
            else:
                print("hold 4")
                print("""take no action -> Hold""")
                action = "Held"
        
        
        
        elif self.signal =='Short':
            
            print("caputrd by Short")
            sell_units = single_trade_amount/tick2
            buy_units = single_trade_amount/tick1
            
            if self.signal == 'Short' and  self.signal != self.prev:
                print("short 1")
                if self.current_pos == 'bought':
                    self.value_2 = self.sell_units * tick2
                    self.value_1 = self.buy_units * tick1
                    self.close_out()
                elif self.current_pos == 'empty':
                    
                    print("short 2")


                    #change tick 2 to actual price (not b*tick2)!!
                    print("Went short: sold",sell_units,"units of BTC","at a price of",tick2, "and bought",buy_units,"of b*BCH at a price of",tick1)
                    #self.sold_value = sell_units*tick2
                    #self.bot_value = buy_units*tick1
                    self.sell_units = sell_units
                    self.buy_units = buy_units
                    self.value_2 = self.sell_units * tick2
                    self.value_1 = self.buy_units * tick1

                    self.bought_sold_price = tick2 - tick1
                    self.current_pos = 'sold'
                    action = "Went Short!"

                else:
                    print("short 5")
                    print("current pos must be already sold - check!")
                    action = "Already Short!"
                    self.value_2 = self.sell_units * tick2
                    self.value_1 = self.buy_units * tick1

            else:
                print("short 6")
                print("prev signal must be Short - check!")
                action = "Already Short!"
                self.value_2 = self.sell_units * tick2
                self.value_1 = self.buy_units * tick1
                
                

           
            
            
        
        elif self.signal =='Long':
            
            print("captured by Long")
            sell_units = single_trade_amount/tick1
            buy_units = single_trade_amount/tick2
            
            if self.signal == 'Long' and self.signal != self.prev:
                print("long 1")
                if self.current_pos == 'sold':
                    self.value_2 = self.sell_units * tick1
                    self.value_1 = self.buy_units * tick2
                    self.close_out() 
                    action = "short => close out"
                elif self.current_pos == "empty":
                    
                    print("long 2")
                    

                    #change tick 2 to actual price!!!
                    print("Went Long: sold",sell_units,"units of b*BCH","at a price of",tick1, "and bought",buy_units,"of BTC at a price of",tick2)
                    #self.sold_value = sell_units*tick1
                    #self.bot_value = buy_units*tick2
                    self.sell_units = sell_units
                    self.buy_units = buy_units
                    self.value_2 = self.sell_units * tick1
                    self.value_1 = self.buy_units * tick2

                    self.bought_sold_price = tick2 - tick1
                    self.current_pos = 'bought'
                    action = "Went Long!"
                    print("should be 1000", single_trade_amount)
                    print("tot trade amount", tot_trade_amount)
                        

                   
                else:
                    print("long 5")
                    print("current pos must be already long - check")
                    action = "Already Long!"
                    self.value_2 = self.sell_units * tick1
                    self.value_1 = self.buy_units * tick2
            else:
                print("long 6")
                print("prev signal must be long - check!")
                action = "Already Long!"
                self.value_2 = self.sell_units * tick1
                self.value_1 = self.buy_units * tick2


    
                
        else:
            print("not captured 1")
            print("not captured by buy sell or hold need to fix!")
            
            
        print(self.sell_units)
        print(self.buy_units)
        print('spread:', abs(tick1 - tick2))
        print(ts)
        
        print('R_pnl:', self.rpl)
        #print("tick1: ", tick1, "tick2: ", tick2)
        urpl = (1000 - self.value_2) + (self.value_1 - 1000)
        print('U_pnl:',urpl)
        self._port.loc[len(self._port)] = [ts,self.signal,action,self.value_2,self.value_1,urpl,self.rpl]

            
        
        
        
        self.prev = self.signal
        self.stamp+=1


#create strategy to perform on any pair.
class Strategy(Portfolio):
    
    def __init__(self):
        #use Super to get Portfolio attrs
        Portfolio.__init__(self)
        #price_feed = Data_Puller().fetch_df()
        self.sdev = np.std(q.full_z_coint)
        self.mu = np.mean(q.full_z_coint)
        
    
    #go long / short if +- 1 std, sell when hit mean
    def strat(self):
        
        while q.empty==False:
        
            
            #print('running...')
            #pop lock and drop it...
            btc,bch,ts,z_coint,b_x_bch = q.iloc[0]
            q.drop(q.head(1).index,inplace=True)
                        
            #compare to plus / minus 1 stdev -> generate signal
            if z_coint > self.mu + self.sdev:
                #self.orders.loc[len(self.orders)] = [ts,'Short',btc,bch]
                self.signal = 'Short'
                self.position(ts,b_x_bch,btc,z_coint)
                
            elif z_coint < self.mu - self.sdev:
                #self.orders.loc[len(self.orders)] = [ts,'Long',btc,bch]
                self.signal = 'Long'
                self.position(ts,b_x_bch,btc,z_coint)
                
                            
            
            else:
                #self.orders.loc[len(self.orders)] = [ts,'Hold',btc,bch]
                self.signal = 'Hold'
                self.position(ts,b_x_bch,btc,z_coint)
                
            
            
            
            
            #print(self.current_position)
        
        print('Finished!')
        
            
                
    def get_portfolio(self):
        self._port.set_index('ts',inplace=True)
        #plt.plot(self._port.R_pnl)
        #plt.show()
        #pd.set_option('display.max_rows', 400)
        return self._port.head(360)
        #return self._port
        

        
                
  

if __name__ == "__main__":
    
    import requests
    import numpy as np
    import pandas as pd
    import seaborn as sns
    from scipy import stats
    
# change params in Data_Puller as you want
    x = Data_Puller('BTC','BCH','day',500)
    x.get_data()
    q = x.fetch_df()
    p = Strategy()
    p.strat()
    p.get_portfolio()

