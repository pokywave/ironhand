import numpy as np
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
import sys
import string
import requests
import datetime
import time
import calendar


def dailystats(day, month, year):

    url = 'https://www.basketball-reference.com/friv/dailyleaders.fcgi?month={month}&day={day}&year={year}&type=all'
    page = requests.get(url.format(month=month, day=day, year=year))
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find('table')
    table_body = table.find('tbody')
    table_row = table_body.findAll('tr')

    #certain day there is no game play therefore no table will be found.
    if table == None:
        return None
        
    else:    
        
        #scrap the datas from the table
        dailyleaders = []
        for row in table_row:

            cells = row.findAll('td')
           
            if len(cells) > 0:
                
                player_data = {"Player": str(cells[0].text),
                               "TM": str(cells[1].text),
                               "":cells[2].text,
                               "Opp":str(cells[3].text),
                               "":cells[4].text,
                               "MP":cells[5].text,
                               "FG":int(cells[6].text),
                               "FGA":int(cells[7].text),
                               "FG%":(cells[8].text),
                               "3P":int(cells[9].text),
                               "3PA":int(cells[10].text),
                               "3P%":(cells[11].text),
                               "FT":int(cells[12].text),
                               "FTA":int(cells[13].text),
                               "FT%":(cells[14].text),
                               "ORB":int(cells[15].text),
                               "DRB":int(cells[16].text),
                               "TRB":int(cells[17].text),
                               "AST":int(cells[18].text),
                               "STL":int(cells[19].text),
                               "BLK":int(cells[20].text),
                               "TOV":int(cells[21].text),
                               "PF":int(cells[22].text),
                               "PTS":int(cells[23].text),
                               "GmSc":float(cells[24].text),
                              }        
                dailyleaders.append(player_data)    
        columns = ["Player","TM", "", "Opp", "", "MP", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "FT", "FTA",
                   "FT%", "ORB", "DRB", "TRB", "AST", "BLK", "TOV", "PF", "PTS", "GmSc"]
                                         
        
        data = pd.DataFrame(dailyleaders, columns=columns)
        return data    


def monthlystats(month, year):
    
    dates = calendar.monthrange(year, month)
    
    monthlydata = []
    for date in range(1, dates[1]+1):
        dailyleaders = dailystats(date, month, year)
        monthlydata.append(dailyleaders)
    return monthlydata
        
def calculate_FPTS(df):

    multipliers = {'PTS':1, '3P': 0.5, 'TRB':1.25, 'AST':1.5, 'STL':2, 'BLK':2, 'TOV':-0.5}
    fpts_list = []

    for i in range(df.shape[0]):
        fpts = 0
        double_count = 0
        for stat, multiplier in multipliers.items():
            if stat in ['PTS', 'TRB', 'AST', 'STL', 'BLK']:
                if df.loc[i, stat] >= 10:
                  
                    double_count += 1    
                
            fpts += df.loc[i, stat] * multiplier
            
        if double_count >= 2:
            fpts += 1.5

        if double_count >= 3:
            fpts += 3
        
        fpts_list.append(fpts)
    
    return fpts_list                

   

