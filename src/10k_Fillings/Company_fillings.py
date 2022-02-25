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
import Table_statements as ts


class Company():
    
    def __init__(self):
        self.cik = input("Write the CIK of the company desire: ").strip()
        self.headers = {'User-Agent': '====WRITE YOUR USER AGENT===='}
        self.link = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={self.cik}&type=10-Q&dateb=&owner=include&count=40&search_text="
        
        
    def Edgar_Search_Results(self):
        
        '''This function has the main purpose to run the self.link on the __init__ function. Which redirects
        the user to the main page where all the quarterly fillings are showed depending on the CIK.'''
        
        req = requests.get(self.link, headers=self.headers)
        soup = BeautifulSoup(req.text, 'lxml')
        return soup
        
        
    def Company_Name(self):
        
        company_name = self.Edgar_Search_Results().find_all("span", {"class":"companyName"})
        company_name = str(company_name[0])
        company_name = "".join(company_name)

        company_name = re.findall(r'">(.*?)<acro', company_name)
        company = company_name[0].strip().replace(" ", "_").replace(";" ,"").replace(".", "").strip()

        return company
        
    def Date_Available(self):
        
        '''This function returns from the Edgar_Search_Results page of the SEC the date of the quarterly fillings. 
        So that the user of the function has the possibility to choose from which date he/she wants to get the filling.'''
        
        table = self.Edgar_Search_Results().find_all("table", {"class": "tableFile2"})
        for td in table:
            tr = td.find_all("td")
            text = [str(td) for td in tr]
            links = [re.findall(r">(.*?)<", i) for i in text]
            dates = [i[0] for i in links if len(i[0])==10]
        
        
        return dates
            
    def Filling_Link(self, date = False):
        
        '''Since the interactive site does return JavaScript results and the computer is not able to decode it. The function returns the link of the financial statements depending on the date.
        If date is True the user can choose beyond dates, if False the function returns the latest filling.
        We are now in the interactive datasets'''
        
        table = self.Edgar_Search_Results().find_all("table", {"class": "tableFile2"})        
        for td in table:
            tr = td.find_all("td", {"nowrap":"nowrap"})
            text = [[td] for td in tr]
            links = [text[i][0] for i in range(0, len(text)) if len(text[i][0])>2]

        tr = [[str(tr)] for tr in links]
        
        pattern = r"(/cgi-bin/viewer.*?) "
        url = [[f"https://www.sec.gov/{re.findall(pattern, tr[i][0])}"] for i in range(len(tr))]
        url = [i[0].replace('"', '').replace("/['", "").replace("']", "") for i in url if len(i[0])>100]
        dates = self.Date_Available()
        if date == True:
            '''Interaction with the user'''
            while True:
                dates = self.Date_Available()
                print(f"From which quarter do you want the data?:{dates}")
                print()
                year = input("Write the date of your desire: ").strip().replace("/", "-")
                requested_url = {}
                for date, link in zip(dates, url[:len(dates)]):
                    requested_url[date] = link
                if year in requested_url.keys():
                    url = requested_url[year]
                    return url, year
                    break
                else:
                    print("Not available yet in this version")
        else:
            url = url[0]
            return url, dates[0]
            
                    
    def View_filling_Data(self, datetime=False):
        
        '''return a list of html directions
        [['/Archives/edgar/data/1682852/000168285221000027/R1.htm'],
         ['/Archives/edgar/data/1682852/000168285221000027/R2.htm'],
         ['/Archives/edgar/data/1682852/000168285221000027/R3.htm'],
        ...
        '''
        
        url, date = self.Filling_Link(datetime)
        req = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(req.text, 'lxml')
        found = soup.find_all("script", {"language":"javascript"})
        found = str(found[0])
        found = "".join(found).split(";")
        links = [i for i in found if 74<len(i)<78][:-2]
        links = [links[i].replace(f"reports[{i}+1] = ", "").strip() for i in range(len(links))]
        links = [re.findall(r'"(.*?)"', i) for i in links]
        url = [[f"https://www.sec.gov/{i[0]}"] for i in links]

        return url, date
    
    def correct_statement(self, datetime=False):
        
        '''
        The main usage of this function is to filter out which View_filling_Data links are from which statement.
        This is important because every company has a different format, so it is impossible to find a common filter that works for every company. Thats why it starts reading the headers of the tables of each link.
        If the headers are in the json file under the key of their respective statement that link will be stored. If not, it enters in a while loop where you get asked if the statement is important or not (Notice here it is required to have a bit of topic knowledge, or you Google it) then if you choose the important ones and name it respect to its correct statement, it will save the new naming in the jason file for future usage and will store the link, for the Get Statement Function.
        '''
        
        
        
        
        url, date = self.View_filling_Data(datetime)
        with open("financial_statements.json") as json_file:
            financial_statements = json.load(json_file)
            
        finance_statelist = {}
    
        for j in url:
            print(len(finance_statelist))
            if len(finance_statelist) != 3:
                req = requests.get(j[0], headers=self.headers)
                soup = BeautifulSoup(req.text, 'lxml')
                table = soup.find_all('div', {'style':"width: 200px;"})
                for i in table:
                    tr = i.find_all("strong")
                    titles = [str(title) for title in tr]
                    title = re.findall(r">(.*?)<b", titles[0])
                strings = title[0].lower()

                if strings in financial_statements["income"]:
                    income_tables = j[0]
                    finance_statelist["Income"] = income_tables
                    print(income_tables)
                    print(strings)
                    pass

                elif strings in financial_statements["balance"]:
                    balance_tables = j[0]
                    finance_statelist["Balance"] = balance_tables
                    print(balance_tables)
                    print(strings)
                    pass

                elif strings in financial_statements["cash"]:
                    cashflow_tables = j[0]
                    finance_statelist["Cash"] = cashflow_tables
                    print(cashflow_tables)
                    print(strings)
                    pass

                elif strings in financial_statements["Not_important"]:
                    pass

                else:
                    while True:
                        print("Choose beyond the different statements. In the case you want to see more than one separate your selection with a ','")

                        print(f"Here are the financial statements: {strings}")

                        important_statement = input("Is it important? write YES or NO: ").upper()

                        if important_statement == 'YES':
                            statement = strings
                            select = input("Which of the three does it belong to?[income, balance or cash, None]: ").strip().lower()

                            if select == "income":
                                if strings in [statement]:
                                    income_tables = j[0]
                                    finance_statelist["Income"] = income_tables
                                    financial_statements["income"].append(statement)
                                    with open("financial_statements.json", "w") as json_file:
                                        json.dump(financial_statements, json_file)  
                                    break

                            elif select == "balance":
                                if strings in [statement]:
                                    balance_tables = j[0]
                                    finance_statelist["Balance"] = balance_tables
                                    financial_statements["balance"].append(statement)
                                    with open("financial_statements.json", "w") as json_file:
                                        json.dump(financial_statements, json_file)  
                                    break

                            elif select == "cash":
                                if strings in [statement]:
                                    cashflow_tables = j[0]
                                    finance_statelist["Cash"] = cashflow_tables
                                    financial_statements["cash"].append(statement)
                                    with open("financial_statements.json", "w") as json_file:
                                        json.dump(financial_statements, json_file)
                                    break
                            else:
                                print("The indicated statement is not correct. Try again!")
                            
                            
                            
                        else:
                            financial_statements["Not_important"].append(strings)
                            with open("financial_statements.json", "w") as json_file:
                                json.dump(financial_statements, json_file)
                            break
            else:
                return finance_statelist["Income"], finance_statelist["Balance"], finance_statelist["Cash"], date
                    

    
        
        
    def Get_Statements(self):
        
        '''Here we will access to the individual statements depending on the desires of the users'''
        
        print("Which Statement do you want to analyse?: Income Statement, Balance Sheet, Cash Flow or all of them")
        while True:
            
            statement = input("Insert the statement: ").lower().strip().replace(" ", "").replace("_", ""). replace(" ", "")
            if statement in ["incomestatement", "balancesheet", "cashflow"]:
    
                datetime = input("Do you want to analyze a specific date?. If yes write YES if no write NO: ").upper().strip()

                if datetime == 'YES':
                    datetime=True
                else:
                    datetime = False

                income_tables, balance_tables, cashflow_tables, date = self.correct_statement(datetime)

                company = self.Company_Name()
                print(company)
                if statement == "incomestatement":
                    income_statement = income_tables
                    state = ts.Table_statements(income_statement, 'IS', date, company)
                    return state.statements(date)
                    break

                elif statement == "balancesheet":
                    balance_sheet = balance_tables
                    state = ts.Table_statements(balance_sheet, 'BS', date, company)
                    return state.statements(date)
                    break

                elif statement == "cashflow":
                    cash_flow = cashflow_tables
                    state = ts.Table_statements(cash_flow, 'CF', date, company)
                    return state.statements(date)
                    break

                elif statement in ["allofthem", "all", "thethree", "incomestatementbalancesheetcashflow"]:
                    income_statement = income_tables
                    balance_sheet = balance_tables
                    cash_flow = cashflow_tables
                    state = ts.Table_statements([income_statement, balance_sheet,cash_flow], ['IS', 'BS', 'CF'])
                    return state.dates_datetime()
                    break
            else:
                print(f"Man {statement} is not a correct statement, select the correct one: Income Statement, Balance Sheet, Cash Flow, or All")
            
