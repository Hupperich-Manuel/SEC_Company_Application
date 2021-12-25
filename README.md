# SEC_Company_Application

![Alt Text](https://media.giphy.com/media/Mc1yxvp8fIGuYXHJI0/giphy-downsized-large.gif)

## The story behind the _MEGA PROJECT_

Have you ever wondered why the corporate investors are always one step ahead the individual investors?. The answer is truly not easy, however information is one of the main points, and it is also one of the reasons why i decided to start this project.
Sarting to manage my own investements, and being pretty data oriented led me to think critically abou tthe data I was using for my analysis. thats whhy I wanted to get sure that the input I used for decision making was reliable.
Moreover, why not starting to use machine learning, or even deep learning models in order to get the most insights of the raw data. That is where i started to research about a source that would give me in a structured way the data I needed for every single company that is publicy traded out there. 
Nonetheless, I found myself in monthly subscriptions and creepy data bases. Therefore, i decided to code my own source.


Application that goes from the reliable data extraction of the SEC to the implementation of a machine learning algorithm to predict the performance from the selcted period


```python
import Ratios as r
import pandas as pd
import os
from datetime import datetime
import json
import Company_fillings as cf
```

Now lets get access to the predefined classes for the financial statement extraction (or if already downloaded, for ratio analysis)


```python
company = cf.Company()

#Output: Write the CIK of the company desired: 
```
We will use in this example Apple Inc, therefore the identifyer (CIK) is: 0000320193

```python
company.Get_Statements()
```
![image](https://user-images.githubusercontent.com/67901472/147389658-499c35a9-815b-4828-838b-d35e4db0e5f4.png)
![image](https://user-images.githubusercontent.com/67901472/147389664-1196e7c2-9af6-4a95-90d4-ff120b05bdb7.png)

 If not, you will get downloaded the latest release of Apple Incs Income Statement. On the contrary if you want a specific date, write yes, and you will get all the 10Q sec filling dates since it first release.
 
 ![image](https://user-images.githubusercontent.com/67901472/147389696-b5bd66fd-e6c6-4c41-b856-99950e78eb5f.png)

During the runtime the programm will save every link of the three main financial statements (income statement, balance sheet and cash flow, of course for the sake of efficiency this could be done better).
Finally it will return the dates which are contained in the excel file and also the path where the cleaned statement is going to be located.
Notice that if the file is already mnerged in order to do the ratios analysis, the code will return _Quarter is already merged_
 
 ![image](https://user-images.githubusercontent.com/67901472/147389730-1a20042a-1950-41de-ab34-8f039372e1c2.png)

 
