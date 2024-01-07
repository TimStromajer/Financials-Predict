from re import A
import pandas as pd
import numpy as np


# TODO: ckeck for empty vectors
def createVectors(stockList, numYear=4, trainPercentage=0.7, time="quaterly", predictTime=4):
    allInputs = []
    yAll = []
    for i in stockList:
        # read file, replace empty with nan
        dfIncome = pd.read_csv("data/quaterlyRequest/incomeS/" + i, sep=";", na_values=[" "])
        dfBalance = pd.read_csv("data/quaterlyRequest/balanceS/" + i, sep=";", na_values=[" "])
        dfCashflow = pd.read_csv("data/quaterlyRequest/cashflowS/" + i, sep=";", na_values=[" "])
        # replace nan with 0
        dfIncome = dfIncome.fillna(0)
        dfBalance = dfBalance.fillna(0)
        dfCashflow = dfCashflow.fillna(0)
        # remove first row of income and cashflow if longer
        if len(dfIncome.index) > len(dfBalance.index):
            dfIncome = dfIncome.iloc[1: , :]
        if len(dfCashflow.index) > len(dfBalance.index):
            dfCashflow = dfCashflow.iloc[1: , :]
        # if yearly, sum 4 quaters and delete the rest
        if time == "yearly":
            for i in range(len(dfIncome.index)):
                if i+4 < len(dfIncome.index):
                    dfIncome.iloc[i] = dfIncome.iloc[i:i+4].sum()
                    dfBalance.iloc[i] = dfBalance.iloc[i:i+4].sum()
                    dfCashflow.iloc[i] = dfCashflow.iloc[i:i+4].sum()
                else:
                    dfIncome = dfIncome.drop([i])
                    dfBalance = dfBalance.drop([i])
                    dfCashflow = dfCashflow.drop([i])
            dfIncome = dfIncome.iloc[::4, :]
            dfBalance = dfBalance.iloc[::4, :]
            dfCashflow = dfCashflow.iloc[::4, :]
        # reverse rows
        dfIncome = dfIncome.iloc[::-1]
        dfBalance = dfBalance.iloc[::-1]
        dfCashflow = dfCashflow.iloc[::-1]
        # exclude Date column
        dfIncome = dfIncome.loc[:, dfIncome.columns != 'Date']
        dfBalance = dfBalance.loc[:, dfBalance.columns != 'Date']
        dfCashflow = dfCashflow.loc[:, dfCashflow.columns != 'Date']

        multiplier = 1
        if time == "quaterly":
            multiplier = 4

        # continue if not enough rows
        if len(dfIncome.index) <= numYear * multiplier + predictTime:
            continue

        xAll = []
        for index in range(len(dfIncome.index)):
            xOne = []
            oneInput = []
            for year in range(numYear * multiplier):
                xOne = [*xOne, *dfIncome.iloc[index + year].values, *dfBalance.iloc[index + year].values, *dfCashflow.iloc[index + year].values]
                oneInput.append([*dfIncome.iloc[index + year].values, *dfBalance.iloc[index + year].values, *dfCashflow.iloc[index + year].values])

            # normalize
            maxVal = np.abs(xOne).max()
            xOne = xOne / maxVal
            oneInput /= maxVal

            # get column 16 - net profit
            yOne = dfIncome.iloc[index + numYear * multiplier + predictTime - 1, 15] / maxVal
            yAll.append(yOne)

            xAll.append(xOne)
            allInputs.append(oneInput)
            if (index + numYear * multiplier + predictTime == len(dfIncome.index)):
                break
        
    allInputs = np.array(allInputs)
    yAll = np.array(yAll)
    xTrain = allInputs[:int(allInputs.shape[0] * trainPercentage)]
    xTest = allInputs[int(allInputs.shape[0] * trainPercentage):]
    yTrain = yAll[:int(allInputs.shape[0] * trainPercentage)]
    yTest = yAll[int(allInputs.shape[0] * trainPercentage):]
    return xTrain, yTrain, xTest, yTest


def getLastVector(stockList, numYear=4, time="quaterly"):
    multiplier = 1
    if time == "quaterly":
        multiplier = 4
    allInputs = []
    for i in stockList:
        # read file, replace empty with nan
        dfIncome = pd.read_csv("data/quaterlyRequest/incomeS/" + i, sep=";", na_values=[" "])
        dfBalance = pd.read_csv("data/quaterlyRequest/balanceS/" + i, sep=";", na_values=[" "])
        dfCashflow = pd.read_csv("data/quaterlyRequest/cashflowS/" + i, sep=";", na_values=[" "])
        # remove first row of income and cashflow if longer
        if len(dfIncome.index) > len(dfBalance.index):
            dfIncome = dfIncome.iloc[1: , :]
        if len(dfCashflow.index) > len(dfBalance.index):
            dfCashflow = dfCashflow.iloc[1: , :]
        # if yearly sum 4 quaters and delete the rest
        if time == "yearly":
            for j in range(len(dfIncome.index)):
                if j+4 < len(dfIncome.index):
                    dfIncome.iloc[j] = dfIncome.iloc[j:j+4].sum()
                    dfBalance.iloc[j] = dfBalance.iloc[j:j+4].sum()
                    dfCashflow.iloc[j] = dfCashflow.iloc[j:j+4].sum()
                else:
                    dfIncome = dfIncome.drop([j])
                    dfBalance = dfBalance.drop([j])
                    dfCashflow = dfCashflow.drop([j])
            dfIncome = dfIncome.iloc[::4, :]
            dfBalance = dfBalance.iloc[::4, :]
            dfCashflow = dfCashflow.iloc[::4, :]
        # reverse rows
        dfIncome = dfIncome.iloc[::-1]
        dfBalance = dfBalance.iloc[::-1]
        dfCashflow = dfCashflow.iloc[::-1]
        # remove all but last numYear rows
        dfIncome = dfIncome.iloc[-numYear * multiplier:]
        dfBalance = dfBalance.iloc[-numYear * multiplier:]
        dfCashflow = dfCashflow.iloc[-numYear * multiplier:]
        # exclude Date column
        dfIncome = dfIncome.loc[:, dfIncome.columns != 'Date']
        dfBalance = dfBalance.loc[:, dfBalance.columns != 'Date']
        dfCashflow = dfCashflow.loc[:, dfCashflow.columns != 'Date']
        # replace nan with 0
        dfIncome = dfIncome.fillna(0)
        dfBalance = dfBalance.fillna(0)
        dfCashflow = dfCashflow.fillna(0)

        if len(dfIncome.index) < numYear * multiplier:
            continue

        xAll = []
        xOne = []
        oneInput = []
        for year in range(numYear * multiplier):
            xOne = [*xOne, *dfIncome.iloc[year].values, *dfBalance.iloc[year].values, *dfCashflow.iloc[year].values]
            oneInput.append([*dfIncome.iloc[year].values, *dfBalance.iloc[year].values, *dfCashflow.iloc[year].values])

        # normalize
        maxVal = np.abs(xOne).max()
        xOne = xOne / maxVal
        oneInput /= maxVal

        xAll.append(xOne)
        allInputs.append(oneInput)
    
    allInputs = np.array(allInputs)
    xTrain = allInputs[:int(allInputs.shape[0])]
    return xTrain


# xTrain, yTrain, xTest, yTest = createVectors(["AAPL.txt"], numYear=4, trainPercentage=0.7, time="quaterly", predictTime=4)
# print(yTrain)

# xVal = getLastVector(["AAPL.txt"], numYear=4, time="quaterly")