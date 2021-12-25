import requests
import pandas as pd
from bs4 import BeautifulSoup
from openpyxl import Workbook, workbook
import regex as re
import lxml.html as lh
import os
import xlsxwriter
from datetime import datetime
import json
import Clean_Statements as cs


class Table_statements():
    
    def __init__(self, url, statement_required, date, company):
        
        self.url = url
        self.headers = self.headers = {'User-Agent': '====WRITE YOUR USER AGENT===='}  
        self.req = requests.get(self.url, headers=self.headers)
        self.soup = BeautifulSoup(self.req.text, 'lxml')

        self.table = self.soup.find_all('table', {'class':"report", 'border':'0', 'cellspacing':'2'})
        self.statement_required = statement_required
        self.date = date
        self.company = company

        
    def dates_datetime(self):    

        '''Gets the dates of the soup in Jan. 21 2019 format '''
        dates = []
        for tr in self.table:
            td = tr.find_all('th')
            row = [tr.text for tr in td]
            dates.append(row)
        

        if self.statement_required == 'IS':
            if len(row)==4:
                dates = [row[2], row[3]]
                return dates
            else:
                dates = [row[3], row[4], row[5], row[6]]
                return dates
        
        elif self.statement_required == 'CF':
            dates = [dates[0][2], dates[0][3]]
            return dates
        
        elif self.statement_required == 'BS':
            dates = [dates[0][1].strip(), dates[0][2].strip()]
            return dates
            
        elif ('IS' in self.statement_required) and ('BS' in self.statement_required) and ('CF' in self.statement_required):
            dates_IS = [row[3], row[4]]
            dates_BS = [dates[0][1], dates[0][2]]
            dates_CF = [dates[0][2], dates[0][3]]
            return dates_IS, dates_BS, dates_CF
    
    def date_strings(self, sort=False, statement = 'IS'):

        '''Enter in datetime format'''
        
        #For Income Statement
        if statement == 'IS':

            if sort == True:
                '''Only True if a list of dates in string format is being given'''
                dates = [[datetime.strptime(i, '%m/%Y') for i in j] for j in self.dates_datetime()]
                dates.sort()
                dates = [[datetime.strftime(i, '%m/%Y') for i in j] for j in self.dates_datetime()]
            else:
                dates = [datetime.strptime(j, '%b. %d, %Y') for j in self.dates_datetime()]
                dates = [j.strftime('%m/%Y') for j in dates]
                
            
            return dates
        
        if statement == 'CF':

            if sort == True:
                '''Only True if a list of dates in string format is being given'''
                dates = [[datetime.strptime(i, '%m/%Y') for i in j] for j in self.dates_datetime()]
                dates.sort()
                dates = [[datetime.strftime(i, '%m/%Y') for i in j] for j in self.dates_datetime()]
            else:
                dates = [datetime.strptime(j, '%b. %d, %Y') for j in self.dates_datetime()]
                dates = [j.strftime('%m/%Y') for j in dates]
            
            return dates
                
        #For Balance Sheet
        elif statement == 'BS':

            if sort == True:
                '''Only True if a list of dates in string format is being given'''
                dates = [[datetime.strptime(i, '%m/%Y') for i in j] for j in self.dates_datetime()]
                dates.sort()
                dates = [[datetime.strftime(i, '%m/%Y') for i in j] for j in self.dates_datetime()]
            else:
                dates = [datetime.strptime(j, '%b. %d, %Y') for j in self.dates_datetime()]
                dates = [j.strftime('%m/%Y') for j in dates]
            
            return dates
                
            
    
    
    def divide(self, statements, n):
        '''Gets a list and divides it so that it can be integrated in a dataframe'''
        for j in range(0, len(statements), n):
            yield statements[j:j+n]
            
            
            
            
    def download(self, df, state):
        
        path =  f"====PATH FOR THE UNCLEANED STATEMENTS===={self.company}/"+str(state)+f"{self.company}.xlsx"
        
        if os.path.isdir(f'====PATH FOR THE UNCLEANED STATEMENTS===={self.company}') == True:
            
            if os.path.isfile(path) == True:
                try:
                    with pd.ExcelWriter(path ,engine='openpyxl', mode='a') as writer:
                        df.to_excel(writer, sheet_name=str(self.date))
                except FileNotFoundError:
                    print("No FIle")
                    
            else:
                try:
                    with pd.ExcelWriter(path ,engine='openpyxl', mode='w') as writer:
                        df.to_excel(writer, sheet_name=str(self.date))
                except FileNotFoundError:
                    print("No FIle")
                
        else:
        
            try:
                os.mkdir(f'====PATH FOR THE UNCLEANED STATEMENTS===={self.company}')
                os.mkdir(f'====PATH FOR THE CLEANED STATEMENTS===={self.company}')
                with pd.ExcelWriter(path ,engine='openpyxl', mode='w') as writer:
                    df.to_excel(writer, sheet_name=str(self.date))
            except FileNotFoundError:
                print("Not worked")


    
    def statements(self, dates):


        '''scraps the table returned by soup in order to get every table in the html. It is more efficient that thhe previous one as it get 
        all the tables and does not require the continuously changing id of every table'''

        statements = []
        for tr in self.table:
            td = tr.find_all('td')
            row = [tr.text for tr in td]
            statements.append(row)
            
        if "" in statements[0]:
            n=1
            
        elif (len(self.date_strings())==2) and (self.statement_required =="IS"):
            n=-2
        else:
            n=0
        

        '''Returns the raw statements'''
        
        if self.statement_required == 'IS':
            m = list(self.divide(statements[0], 5+n))#converts the statements output into a nice list which can then be converted into a dataframe
            income_statement = pd.DataFrame(m)
            if len(income_statement.columns) == 6:
                income_statement.drop([1], 1, inplace=True)
            if len(self.date_strings()) == 2:
                income_statement.columns = ['Account', self.date_strings()[0], self.date_strings()[1]]
            
            else:
                income_statement.columns = ['Account', self.date_strings()[0], self.date_strings()[1], self.date_strings()[2]+str("6_months"), self.date_strings()[3]+str("6_months")]
        
            income_statement.set_index(['Account'], inplace=True)
            self.download(income_statement, self.statement_required)
            state = cs.Clean_Statements(income_statement, self.statement_required, str(self.date), self.company)
            return state.Cleaning()
            
        
        elif self.statement_required == 'BS':
            
            m = list(self.divide(statements[0], 3+n))#converts the statements output into a nice list which can then be converted into a dataframe
            balance_sheet = pd.DataFrame(m)
            if len(balance_sheet.columns) == 4:
                balance_sheet.drop([1], 1, inplace=True)
            print(balance_sheet.columns)
            balance_sheet.columns = ['Account', self.date_strings(statement='BS')[0], self.date_strings(statement='BS')[1]]
            balance_sheet.set_index(['Account'], inplace=True)
            self.download(balance_sheet, self.statement_required)
            state = cs.Clean_Statements(balance_sheet, self.statement_required, str(self.date), self.company)
            return state.Cleaning()

            
            
        elif self.statement_required == 'CF':
            
            m = list(self.divide(statements[0], 3+n))#converts the statements output into a nice list which can then be converted into a dataframe
            cashflow = pd.DataFrame(m)
            if len(cashflow.columns) == 4:
                cashflow.drop([1], 1, inplace=True)
            cashflow.columns = ['Account', self.date_strings()[0], self.date_strings()[1]]
            cashflow.set_index(['Account'], inplace=True)
            self.download(cashflow, self.statement_required)
            state = cs.Clean_Statements(cashflow, self.statement_required, str(self.date), self.company)
            return state.Cleaning()

          
            
        elif ('IS' in self.statement_required) and ('BS' in self.statement_required) and ('CF' in self.statement_required):
            
            m = list(self.divide(statements[0], 5+n))
            income_statement = pd.DataFrame(m)
            income_statement.drop([3, 4], 1, inplace=True)
            income_statement.columns = ['Account', self.date_strings()[0], self.date_strings()[1]]
            income_statement.set_index(['Account'], inplace=True)
            self.download(income_statement, self.statement_required)

                
            m = list(self.divide(statements[0], 3+n))
            balance_sheet = pd.DataFrame(m)
            balance_sheet.columns = ['Account', self.date_strings(statement='BS')[0], self.date_strings(statement='BS')[1]]
            balance_sheet.set_index(['Account'], inplace=True)
            self.download(balance_sheet, self.statement_required)

                
                
            m = list(self.divide(statements[0], 3+n))
            cashflow = pd.DataFrame(m)
            cashflow.drop([3, 4], 1, inplace=True)
            cashflow.columns = ['Account', self.date_strings()[0], self.date_strings()[1]]
            cashflow.set_index(['Account'], inplace=True)
            self.download(cashflow, self.statement_required)

  