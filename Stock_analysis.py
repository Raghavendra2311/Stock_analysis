# -*- coding: utf-8 -*-
"""
Created on Mon May 17 17:47:11 2021

@author: RAGHAVENDRA
"""

import yfinance as yf
import pandas as pd
import numpy as np
# import yahoo_finance as yhoo
import matplotlib.pyplot as plt
# from yahoo_finance import Share
import csv
import datetime
import cufflinks as cf
import plotly.offline
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)
import time
import datetime
import os
from IPython.display import clear_output
import smtplib
from yahoo_fin import stock_info as si
import plotly.graph_objects as go
from plotly.offline import plot
pd.set_option('float_format', '{:f}'.format)


def name_of_company(ticker):
    """
    This function returns the long name of the company
    """
    print("Name: ",yf.Ticker(ticker).info['longName'])
    
def avg_rev(ticker):
    """
    This Function provides the average Revenue of the company
    """
    print("The average revenue of",ticker,"is ₹",yf.Ticker(ticker).calendar.loc['Revenue Average'][0],"on",yf.Ticker(ticker).calendar.loc['Earnings Date'][0])
    
def social_score(ticker):
    """
    This function provides the social score of the company
    """
    soc_score = yf.Ticker(ticker).sustainability.loc['socialScore']
    soc_score = str(soc_score)
    name = yf.Ticker(ticker).info['longName']
    print("The social score of "+name+" is "+soc_score)
    
def env_score(ticker):
    """
    This function provides the environmental score of the company
    """
    env_score_ = yf.Ticker(ticker).sustainability.loc['environmentScore']
    print("The Environmental score of {} is {}".format(yf.Ticker(ticker).info['longName'],env_score_))

def dividend_(ticker):
    '''
    This function returns Dividends provided by the company over the years-[if provided].
    '''
    if yf.Ticker(ticker).dividends.empty:
        print("The Company never offered Dividend to its stake holders")
    else:
        divi = pd.DataFrame(yf.Ticker(ticker).dividends)
        return divi
    
def balance_sheet(ticker):
    """
    This function returns the balance sheet in the form of Dataframe
    """
    balance_s = yf.Ticker(ticker).balance_sheet
    return balance_s

def cash_flow(ticker):
    """
    This function returns the Cash Flow in the form of Dataframe
    """
    cash_f = yf.Ticker(ticker).cashflow
    return cash_f

def financials(ticker):
    """
    This function returns the financials in the form of Dataframe
    """
    fin = yf.Ticker(ticker).financials
    return fin
    
def splits_(ticker):
    '''
    This function returns splits provided by the company over the years-[if provided].
    '''
    if yf.Ticker(ticker).splits.empty:
        print("The Company never offered Dividend to its stake holders")
    else:
        split = pd.DataFrame(yf.Ticker(ticker).splits)
        return split
    
def shareholders(ticker):
    """
    This function provides the top 5 institutional holders
    """
    return yf.Ticker(ticker).get_institutional_holders().head().drop('Date Reported',axis=1)

def majorholders(ticker):
    """
    This function provides the major holders
    """
    return yf.Ticker(ticker).major_holders()

def q_balancesheet(ticker):
    """
    This function provides the quarterly balance sheet
    """
    return yf.Ticker(ticker).quarterly_balance_sheet

def q_cashflow(ticker):
    """
    This function provides the quarterly cashflow
    """
    return yf.Ticker(ticker).quarterly_cashflow

def q_fin(ticker):
    """
    This function provides the quarterly balance sheet
    """
    return yf.Ticker(ticker).quarterly_financials

def cur_price_live(ticker):
    """
    This provides the current market price of the stock. It has a minor lag
    """
    while True:
        now = datetime.datetime.now()
        time1 = now.strftime("%H:%M:%S")
        tickers = yf.Ticker(ticker)
        todays_data = tickers.history(period='1d')
        return (todays_data['Close'][0])
        time.sleep(2)
        
def graph_open_close(ticker):
    """
    This graph provides the graph of opening and closing prices
    """
    tickers = yf.Ticker(ticker)
    df = tickers.history(period='1y')
    
    df.columns = [col.replace(ticker+".", "") for col in df.columns]
    
    # Create figure
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(x=list(df.index), y=list(df['High'])))
    
    # Set title
    fig.update_layout(
        title_text="Time series with range slider and selectors"
    )
    
    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    
    plot(fig,auto_open=True,renderer="console")
  

def open_price(ticker):
    """
    This function provides the opening price
    """
    df= yf.Ticker(ticker).info['open']
    print("Opening price: ",df)
    
def last_close(ticker):
    """
    This function provides the last closing price
    """
    df= yf.Ticker(ticker).info['previousClose']
    print("Previous Closing price: ",df)

def info_func(ticker_name):
    '''
    This Functions returns all the information of the Ticker
    '''
    T_name = yf.Ticker(ticker_name)
    key_list = list(T_name.info.keys())
    val_list = list(T_name.info.values())
    df = pd.DataFrame(data=val_list,index=key_list)
    info_df  = df.transpose().rename(index={0:ticker_name})
    
    return info_df.transpose()

def fifty_two(ticker):
    print("52 week high:",yf.Ticker(ticker).info['fiftyTwoWeekHigh'])
    print("52 week low:",yf.Ticker(ticker).info['fiftyTwoWeekLow'])
    tickers = yf.Ticker(ticker)
    todays_data = tickers.history(period='1y')
    year_old_price = todays_data['Close'][0]
    current = si.get_live_price(ticker)
    print("52 week change: {:.2f} %".format(((current - year_old_price)*100)/year_old_price))
    
def market_cap(ticker):
    """
    This function provides the total value of all the shares of the company
    """
    vol = yf.Ticker(ticker).info['volume']
    price = yf.Ticker(ticker).history(period='1d')['Close'][0]
    mark_cap = vol*price
    name = yf.Ticker(ticker).info['longName']
    print("The total market cap of {} is ₹{}".format(name,mark_cap))
    

    

    
def main_func(ticker):
    ticker = ticker.capitalize()
    name_of_company(ticker)
    info_func(ticker)
    social_score(ticker)
    env_score(ticker)
    fifty_two(ticker)
    avg_rev(ticker)
    market_cap(ticker)
    open_price(ticker)
    last_close(ticker)

#main_func('SBIN.NS')

#graph_open_close('RELIANCE.NS')

#div = dividend_(ticker)
#share_h = shareholders(ticker)
#spl = splits_(ticker)
#bal = balance_sheet(ticker)
#fi = financials(ticker)
#ca = cash_flow(ticker)
#info = info_func(ticker)
#in_holder = shareholders(ticker)
#maj_holders = majorholders(ticker)
#qbal = q_balancesheet(ticker)
#qfin = q_fin(ticker)
#qcash = q_cashflow(ticker)


################################################################

def send_mail(reciever_id,msg):
    x = smtplib.SMTP('smtp.gmail.com',587)
    x.starttls() 
    x.login("stock.analysis.alert@gmail.com", "PBL@2021")
    x.sendmail('stock.analysis.alert@gmail.com',reciever_id,msg)
    
def price_alert(x):
    stop_loss = int(input("Enter the stop loss:"))
    msg = "Price Alert: {}!".format(stop_loss)
    while True:
        now = datetime.datetime.now()
        time1 = now.strftime("%H:%M:%S")
        tickers = yf.Ticker(x)
        todays_data = tickers.history(period='1d')
        if (todays_data['Close'][0]) <= stop_loss:
            print(msg)
            send_mail('raghavendrakharosekar23@gmail.com','PRICE ALERT STOP LOSS TRIGGERED')
            break
        time.sleep(2) 

























    
