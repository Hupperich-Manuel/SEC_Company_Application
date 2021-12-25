from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from pandas import ExcelWriter
from openpyxl import load_workbook
from datetime import datetime
import re
import os
import glob
import openpyxl
import matplotlib.pyplot as plt


class Ratios():
    
    def __init__(self):
        
        print("Which company do you want to analyze?: {}".format(os.listdir("====PATH FOR THE CLEANED STATEMENTS====")))
        self.path = "====PATH FOR THE CLEANED STATEMENTS===="
        self.directory = input("Paste the compnay: ")
        self.incomestatement_path = os.listdir(self.path+str(self.directory))[-1]
        self.balancesheet_path = os.listdir(self.path+str(self.directory))[-3]
        self.cashflow_path = os.listdir(self.path+str(self.directory))[-2]
        self.income_merged_statements = pd.read_excel(self.path+str(self.directory)+"/"+self.incomestatement_path)
        self.balance_merged_statements = pd.read_excel(self.path+str(self.directory)+"/"+self.balancesheet_path)
        self.cash_merged_statements = pd.read_excel(self.path+str(self.directory)+"/"+self.cashflow_path)
       
        
    def ratios(self):
        
        '''Returns the ratios of the selected company. Notice the index adjustments are
        done for Apple, since for others, Natural Language Processing would be required 
        '''
        
        income_statement = self.income_merged_statements.iloc[:-6]
        balance_sheet = self.balance_merged_statements
        cash_flow = self.cash_merged_statements
        
        balance_sheet.iloc[19, balance_sheet.columns.get_loc("Account")] = "Short Term debt"
        balance_sheet.iloc[22, balance_sheet.columns.get_loc("Account")] = "Long Term debt"
        
        ratios = {"Current Ratio": balance_sheet.iloc[7].values[1:]/balance_sheet.iloc[20].values[1:],
          "Acid Ratio": (balance_sheet.iloc[7].values[1:]-balance_sheet.iloc[4].values[1:])/balance_sheet.iloc[20].values[1:],
          "Cash Ratio": balance_sheet.iloc[1].values[1:]/balance_sheet.iloc[20].values[1:],
          "Operating Cash Flow Ratio": cash_flow.iloc[17].values[1:]/balance_sheet.iloc[20].values[1:],
          "Debt to Equity Ratio": balance_sheet.iloc[25].values[1:]/balance_sheet.iloc[31].values[1:],
          "Debt Ratio": balance_sheet.iloc[25].values[1:]/balance_sheet.iloc[13].values[1:],
          "Debt Service Coverage Ratio": income_statement.iloc[7].values[1:]/(balance_sheet.iloc[22].values[1:]+balance_sheet.iloc[19].values[1:]),
          "Asset Turnover Ratio": income_statement.iloc[0].values[1:]/income_statement.iloc[13].values[1:],
          "Inventory Turnover Ratio": income_statement.iloc[1].values[1:]/balance_sheet.iloc[4].values[1:],
          "Gross Margin Ratio":  income_statement.iloc[2].values[1:]/income_statement.iloc[0].values[1:],
          "Operating Margin Ratio": income_statement.iloc[7].values[1:]/income_statement.iloc[0].values[1:],
          "Return on Assets Ratio": income_statement.iloc[11].values[1:]/balance_sheet.iloc[13].values[1:],
          "Return on Equity Ratio": income_statement.iloc[11].values[1:]/balance_sheet.iloc[31].values[1:],
          "Book per Share Ratio": balance_sheet.iloc[31].values[1:]/income_statement.iloc[17].values[1:],
          "Earnings per share Ratio": income_statement.iloc[11].values[1:]/income_statement.iloc[17].values[1:]
          }
        
        
        
        return pd.DataFrame(ratios, index=income_statement.columns[1:])