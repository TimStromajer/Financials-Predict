import requests
import json
from os.path import exists
import os

# cwd = os.getcwd()  # Get the current working directory (cwd)
# files = os.listdir(cwd + "/data/quaterlyRequest/cashflowsS")  # Get all the files in that directory
# print("Files in %r: %s" % (cwd, files))
# open(cwd + "/data/quaterlyRequest/cashflowsS/AAPL.txt")
# a

def getDataRequest(stockUrl, statement="income-statement", time="quaterlyRequest"):

    stock = stockUrl.split("/")[-3]

    if statement == "income-statement" and exists("data/" + time + "/incomeS/" + stock + ".txt"):
        print(stock + " income-statement exists")
        return
    if statement == "balance-sheet" and exists("data/" + time + "/balanceS/" + stock + ".txt"):
        print(stock + " balance-sheet exists")
        return
    if statement == "cash-flow-statement" and exists("data/" + time + "/cashflowS/" + stock + ".txt"):
        print(stock + " cash-flow-statement exists")
        return

    x = requests.get(stockUrl + '/' + statement + '?freq=Q')
    html = x.content.decode("utf-8")
    dict = html.split("var originalData = ", 1)[1].split("\n", 1)[0]
    dict = dict[:-2]
    dict = json.loads(dict)

    f = ""
    columns = ""
    if statement == "income-statement":
        f = open("data/" + time + "/incomeS/" + stock + ".txt", "a")
        columns = (""
            "Date; "
            "Revenue; "
            "Cost Of Goods Sold; "
            "Gross Profit; "
            "Research And Development Expenses; "
            "SG&A Expenses; "
            "Other Operating Income Or Expenses; "
            "Operating Expenses; "
            "Operating Income; "
            "Total Non-Operating Income/Expense; "
            "Pre-Tax Income; "
            "Income Taxes; "
            "Income After Taxes; "
            "Other Income; "
            "Income From Continuous Operations; "
            "Income From Discontinued Operations; "
            "Net Income; "
            "EBITDA; "
            "EBIT; "
            "Basic Shares Outstanding; "
            "Shares Outstanding; "
            "Basic EPS; "
            "EPS - Earnings Per Share"
            "\n"
        )
    elif statement == "balance-sheet":
        f = open("data/" + time + "/balanceS/" + stock + ".txt", "a")
        columns = (""
            "Date; "
            "Cash On Hand; "
            "Receivables; "
            "Inventory; "
            "Pre-Paid Expenses; "
            "Other Current Assets; "
            "Total Current Assets; "
            "Property, Plant, And Equipment; "
            "Long-Term Investments; "
            "Goodwill And Intangible Assets; "
            "Other Long-Term Assets; "
            "Total Long-Term Assets; "
            "Total Assets; "
            "Total Current Liabilities; "
            "Long Term Debt; "
            "Other Non-Current Liabilities; "
            "Total Long Term Liabilities; "
            "Total Liabilities; "
            "Common Stock Net; "
            "Retained Earnings (Accumulated Deficit); "
            "Comprehensive Income; "
            "Other Share Holders Equity; "
            "Share Holder Equity; "
            "Total Liabilities And Share Holders Equity"
            "\n"
        )
    elif statement == "cash-flow-statement":
        f = open("data/" + time + "/cashflowS/" + stock + ".txt", "a")
        columns = (""
            "Date; "
            "Net Income/Loss; "
            "Total Depreciation And Amortization - Cash Flow; "
            "Other Non-Cash Items; "
            "Total Non-Cash Items; "
            "Change In Accounts Receivable; "
            "Change In Inventories; "
            "Change In Accounts Payable; "
            "Change In Assets/Liabilities; "
            "Total Change In Assets/Liabilities; "
            "Cash Flow From Operating Activities; "
            "Net Change In Property, Plant, And Equipment; "
            "Net Change In Intangible Assets; "
            "Net Acquisitions/Divestitures; "
            "Net Change In Short-term Investments; "
            "Net Change In Long-Term Investments; "
            "Net Change In Investments - Total; "
            "Investing Activities - Other; "
            "Cash Flow From Investing Activities; "
            "Net Long-Term Debt; "
            "Net Current Debt; "
            "Debt Issuance/Retirement Net - Total; "
            "Net Common Equity Issued/Repurchased; "
            "Net Total Equity Issued/Repurchased; "
            "Total Common And Preferred Stock Dividends Paid; "
            "Financial Activities - Other; "
            "Cash Flow From Financial Activities; "
            "Net Cash Flow; "
            "Stock-Based Compensation; "
            "Common Stock Dividends Paid"
            "\n"
        )

    f.write(columns)

    dataArray = [[key] for key in dict[0]]
    dataArray = dataArray[2:]

    for row in dict:
        for i, key in enumerate(row):
            if key == "field_name" or key == "popup_icon":
                continue
            if row[key] == "":
                row[key] = 0
            dataArray[i - 2].append(round(float(row[key]), 2))

    for time in dataArray:
        row = ""
        for amount in time:
            row += str(amount) + "; "
        row = row[:-2]
        f.write(row + "\n")



f = open("data/SandPNames.txt", "r")
Lines = f.readlines()
stockList = []
for i in Lines:
    stockList.append(i.strip())

for s in stockList:
    print(s)
    getDataRequest(s, statement="income-statement")
    getDataRequest(s, statement="balance-sheet")
    getDataRequest(s, statement="cash-flow-statement")