import requests
from os.path import exists


def getData(stock, statement="income", time="quaterly"):

    if statement == "income" and exists("data/" + time + "/incomeS/" + stock + ".txt"):
        print(stock + "income exists")
        return
    if statement == "balance" and exists("data/" + time + "/balanceS/" + stock + ".txt"):
        print(stock + " balance-statement exists")
        return
    if statement == "cash" and exists("data/" + time + "/cashflowS/" + stock + ".txt"):
        print(stock + " cash-flow-statement exists")
        return

    url = "https://macrotrends-finance.p.rapidapi.com/" + statement

    querystring = {"symbol": stock, "freq":"Q"}

    headers = {
        "X-RapidAPI-Key": "APIKEY",
        "X-RapidAPI-Host": "macrotrends-finance.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    resJson = response.json()
    
    years = 0
    f = ""
    columns = ""
    newestYear = -1
    if statement == "income":
        years = len(resJson["Revenue"])
        newestYear = list(resJson["Revenue"].keys())[0][:4]
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
    elif statement == "balance":
        years = len(resJson["Cash On Hand"])
        newestYear = list(resJson["Cash On Hand"].keys())[0][:4]
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
    elif statement == "cash":
        years = len(resJson["Net Income/Loss"])
        newestYear = list(resJson["Net Income/Loss"].keys())[0][:4]
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

    for i in range(int(newestYear), int(newestYear) - years, -1):
        if statement == "income":
            date = list(resJson["Revenue"].keys())[int(newestYear) - i]
            # date = str(i) + date[4:]
            f.write(date + "; " + 
                    str(resJson["Revenue"][date]) + "; " + 
                    str(resJson["Cost Of Goods Sold"][date]) + "; " +  
                    str(resJson["Gross Profit"][date]) + "; " +  
                    str(resJson["Research And Development Expenses"][date]) + "; " + 
                    str(resJson["SG&A Expenses"][date]) + "; " + 
                    str(resJson["Other Operating Income Or Expenses"][date]) + "; " + 
                    str(resJson["Operating Expenses"][date]) + "; " +  
                    str(resJson["Operating Income"][date]) + "; " +  
                    str(resJson["Total Non-Operating Income/Expense"][date]) + "; " + 
                    str(resJson["Pre-Tax Income"][date]) + "; " +  
                    str(resJson["Income Taxes"][date]) + "; " +  
                    str(resJson["Income After Taxes"][date]) + "; " + 
                    str(resJson["Other Income"][date]) + "; " + 
                    str(resJson["Income From Continuous Operations"][date]) + "; " + 
                    str(resJson["Income From Discontinued Operations"][date]) + "; " + 
                    str(resJson["Net Income"][date]) + "; " + 
                    str(resJson["EBITDA"][date]) + "; " + 
                    str(resJson["EBIT"][date]) + "; " + 
                    str(resJson["Basic Shares Outstanding"][date]) + "; " + 
                    str(resJson["Shares Outstanding"][date]) + "; " +
                    str(resJson["Basic EPS"][date]) + "; " + 
                    str(resJson["EPS - Earnings Per Share"][date]) +
                    "\n")
        elif statement == "balance":
            date = list(resJson["Cash On Hand"].keys())[int(newestYear) - i]
            # date = str(i) + date[4:]
            f.write(date + "; " + 
                    str(resJson["Cash On Hand"][date]) + "; " + 
                    str(resJson["Receivables"][date]) + "; " + 
                    str(resJson["Inventory"][date]) + "; " + 
                    str(resJson["Pre-Paid Expenses"][date]) + "; " + 
                    str(resJson["Other Current Assets"][date]) + "; " + 
                    str(resJson["Total Current Assets"][date]) + "; " + 
                    str(resJson["Property, Plant, And Equipment"][date]) + "; " + 
                    str(resJson["Long-Term Investments"][date]) + "; " + 
                    str(resJson["Goodwill And Intangible Assets"][date]) + "; " + 
                    str(resJson["Other Long-Term Assets"][date]) + "; " + 
                    str(resJson["Total Long-Term Assets"][date]) + "; " + 
                    str(resJson["Total Assets"][date]) + "; " + 
                    str(resJson["Total Current Liabilities"][date]) + "; " + 
                    str(resJson["Long Term Debt"][date]) + "; " + 
                    str(resJson["Other Non-Current Liabilities"][date]) + "; " + 
                    str(resJson["Total Long Term Liabilities"][date]) + "; " + 
                    str(resJson["Total Liabilities"][date]) + "; " + 
                    str(resJson["Common Stock Net"][date]) + "; " + 
                    str(resJson["Retained Earnings (Accumulated Deficit)"][date]) + "; " + 
                    str(resJson["Comprehensive Income"][date]) + "; " + 
                    str(resJson["Other Share Holders Equity"][date]) + "; " + 
                    str(resJson["Share Holder Equity"][date]) + "; " + 
                    str(resJson["Total Liabilities And Share Holders Equity"][date]) + 
                    "\n")
        elif statement == "cash":
            date = list(resJson["Net Income/Loss"].keys())[int(newestYear) - i]
            # date = str(i) + date[4:]
            f.write(date + "; " + 
                    str(resJson["Net Income/Loss"][date]) + "; " +
                    str(resJson["Total Depreciation And Amortization - Cash Flow"][date]) + "; " +
                    str(resJson["Other Non-Cash Items"][date]) + "; " +
                    str(resJson["Total Non-Cash Items"][date]) + "; " +
                    str(resJson["Change In Accounts Receivable"][date]) + "; " +
                    str(resJson["Change In Inventories"][date]) + "; " +
                    str(resJson["Change In Accounts Payable"][date]) + "; " +
                    str(resJson["Change In Assets/Liabilities"][date]) + "; " +
                    str(resJson["Total Change In Assets/Liabilities"][date]) + "; " +
                    str(resJson["Cash Flow From Operating Activities"][date]) + "; " +
                    str(resJson["Net Change In Property, Plant, And Equipment"][date]) + "; " +
                    str(resJson["Net Change In Intangible Assets"][date]) + "; " +
                    str(resJson["Net Acquisitions/Divestitures"][date]) + "; " +
                    str(resJson["Net Change In Short-term Investments"][date]) + "; " +
                    str(resJson["Net Change In Long-Term Investments"][date]) + "; " +
                    str(resJson["Net Change In Investments - Total"][date]) + "; " +
                    str(resJson["Investing Activities - Other"][date]) + "; " +
                    str(resJson["Cash Flow From Investing Activities"][date]) + "; " +
                    str(resJson["Net Long-Term Debt"][date]) + "; " +
                    str(resJson["Net Current Debt"][date]) + "; " +
                    str(resJson["Debt Issuance/Retirement Net - Total"][date]) + "; " +
                    str(resJson["Net Common Equity Issued/Repurchased"][date]) + "; " +
                    str(resJson["Net Total Equity Issued/Repurchased"][date]) + "; " +
                    str(resJson["Total Common And Preferred Stock Dividends Paid"][date]) + "; " +
                    str(resJson["Financial Activities - Other"][date]) + "; " +
                    str(resJson["Cash Flow From Financial Activities"][date]) + "; " +
                    str(resJson["Net Cash Flow"][date]) + "; " +
                    str(resJson["Stock-Based Compensation"][date]) + "; " +
                    str(resJson["Common Stock Dividends Paid"][date]) +
                    "\n")

    f.close()


# f = open("data/SandPSymbols.txt", "r")
# Lines = f.readlines()
# stockList = []
# for i in Lines:
#     stockList.append(i.strip())
# skipped = ["QCOM", "META", "BF.B"] #["WRK", "VICI", "T", "SEDG", "NOW", "MSCI", "LOW"]
# for s in stockList:
#     if s in skipped:
#         print(s + " is skipped")
#         continue
#     print(s)
#     getData(s, statement="income-statement")
#     getData(s, statement="balance-statement")
#     getData(s, statement="cash-flow-statement")

a = "BIP"
getData(a, statement="income")