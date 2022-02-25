<h1 align="center">
    <font size="30">
        <u>SEC Company Application</u>
    </font>
</h1>

<p align="center">
  <img src="https://user-images.githubusercontent.com/67901472/155784256-4323f4c5-b13b-449d-b048-79bc59cc519b.png" width=7600", height="400"/>
</p>


[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)
[![GitHub version](https://badge.fury.io/gh/ManuelHupperich%2FStrapDown.js.svg)](https://github.com/ManuelHupperich/StrapDown.js)
[![Github all releases](https://img.shields.io/github/downloads/Hupperich-Manuel/SEC_Company_Application/total.svg)](https://GitHub.com/Hupperich-Manuel/SEC_Company_Application/releases/)
[![Github all releases](https://img.shields.io/github/downloads/Hupperich-Manuel/SEC_Company_Application/total.svg)](https://GitHub.com/Hupperich-Manuel/SEC_Company_Application/releases/)
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
![counter](https://enlg7u0qi4yx26n.m.pipedream.net)                                                                                                                


# Table of Contents
1. [Abstract](#Abstract)
2. [The story behind the Project](#introduction)
3. [How to profit from this work?](#Scope)
4. [How to use it?](#Explanation)


## Abstract
This work entails the required code to extract the SEC 10Q filling from every publicy traded company in the amercian stock market. However, being this a very complex task which requires constant updates, either because companies change they filling format, or because new ones enter into the market, the results obtained with this code should always be evaluated by a professional who has the necessary domain knwoledge to evaluate the accuracy of the data. Moreover, the code is aimed to serve as open source, in order to create a community that enables the individual investors to use to use financial info for their purpose without having to pay for relational information. This code is my first personal big project, therefore a lot of optimization updates could be done, aditionally, not all the companies can be extracted with it, thats why I encourage everyone out there to give me feedback and if so contribute to this project. In this whole analysis we are going to use Apple, as the guiding example, since it is the one which works with data from 2016 onwards, and which is _relatively well organized while concatening the data_ which is not the case for other entities (thats is why the domain knwoledge).


<h1 align="center">
    <font size="22">
        <u>The story behind the Project</u>
    </font>
</h1>

## Introduction

Have you ever wondered why the corporate investors are always one step ahead the individual investors?. The answer is truly not easy, however information is one of the main points, and it is also one of the reasons why i decided to start this project.
Sarting to manage my own investements, and being pretty data oriented led me to think critically abou tthe data I was using for my analysis. thats whhy I wanted to get sure that the input I used for decision making was reliable.
Moreover, why not starting to use machine learning, or even deep learning models in order to get the most insights of the raw data. That is where i started to research about a source that would give me in a structured way the data I needed for every single company that is publicy traded out there. 
Nonetheless, I found myself in monthly subscriptions and creepy data bases. Therefore, i decided to code my own source.



<h1 align="center">
    <font size="22">
        <u>How to profit from this work?</u>
    </font>
</h1>

## Scope

The scope of this project is to get the necesary information to perform several time series analysis on the financial information gathered through the information scrap. These can go from the stock price predictions with machine or deep leraning models till basic descriptive statistics for the more fundamental passionate investor.

In this section we are going to see some applications where this data could be used for.

### Descriptive Statistics

<p align="center">
<kbd>
    <img src= "https://user-images.githubusercontent.com/67901472/148179300-d5bd654e-4bc2-4c27-82d7-e9c883952df3.png" width ="430" height="390">
    <img src= "https://user-images.githubusercontent.com/67901472/148179349-617ca63b-dea1-4ad7-94cf-1101b2a4960c.png", width="430" height="390">
</kbd>
</p>

<h1 align="center">
    <font size="22">
        <u>How to use it?</u>
    </font>
</h1>

## Explanation

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
<kbd>
    <img src= "https://user-images.githubusercontent.com/67901472/147389658-499c35a9-815b-4828-838b-d35e4db0e5f4.png" width ="1000" height="120">
    <img src= "https://user-images.githubusercontent.com/67901472/147389664-1196e7c2-9af6-4a95-90d4-ff120b05bdb7.png", width="1000" height="70">
</kbd>


 If not, you will get downloaded the latest release of Apple Incs Income Statement. On the contrary if you want a specific date, write yes, and you will get all the 10Q sec filling dates since it first release.
 
 <kbd>
    <img src= "https://user-images.githubusercontent.com/67901472/147389696-b5bd66fd-e6c6-4c41-b856-99950e78eb5f.png">
</kbd>


During the runtime the programm will save every link of the three main financial statements (income statement, balance sheet and cash flow, of course for the sake of efficiency this could be done better).
Finally it will return the dates which are contained in the excel file and also the path where the cleaned statement is going to be located.
Notice that if the file is already mnerged in order to do the ratios analysis, the code will return _Quarter is already merged_
 
<p align="center">
<kbd>
  <img src="https://user-images.githubusercontent.com/67901472/147389730-1a20042a-1950-41de-ab34-8f039372e1c2.png" width="500" height="250">
</kbd>
</p>
