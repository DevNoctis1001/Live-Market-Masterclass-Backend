import re


#94165383605 BOT +18 NVDA 100 (Weeklys) 28 MAR 25 114 PUT @1.23LAST=115.78 BID=115.77 ASK=115.78 MARK=115.78 CLOSE=null , ACCOUNT *****530SCHW,
#94165383605 SOLD -20 NVDA 100 (Weeklys) 28 MAR 25 114 CALL @1.23LAST=115.78 BID=115.77 ASK=115.78 MARK=115.78 CLOSE=115.78 , ACCOUNT *****SCsSCHW,

class OrderDetail:
    def __init__(self):
        self.OrderId = ""
        self.Action = ""
        self.Quantity = ""
        self.Symbol = ""
        self.Shares = ""
        self.OptionType = ""
        self.Expiry = ""
        self.Strike = ""
        self.ContractType = ""
        self.ContractPrice = ""
        self.LastPrice = ""
        self.BidPrice = ""
        self.AskPrice = ""
        self.MarkPrice = ""
        self.ClosePrice = ""
        self.Account = ""

    def print(self):        
        print(f"OrderId: {self.OrderId}")
        print(f"Action: {self.Action}")
        print(f"Quantity: {self.Quantity}")
        print(f"Symbol: {self.Symbol}")
        print(f"Shares: {self.Shares}")
        print(f"OptionType: {self.OptionType}")
        print(f"Expiry: {self.Expiry}")
        print(f"Strike: {self.Strike}")
        print(f"ContractType: {self.ContractType}")
        print(f"ContractPrice: {self.ContractPrice}")
        print(f"LastPrice: {self.LastPrice}")
        print(f"BidPrice: {self.BidPrice}")
        print(f"AskPrice: {self.AskPrice}")
        print(f"MarkPrice: {self.MarkPrice}")
        print(f"ClosePrice: {self.ClosePrice}")
        print(f"Account: {self.Account}")

def ParseStringByRe(message) :
    pattern  = r'(#\d+) ([A-Z]+) ([+-]?\d+) ([A-Z]+) (\d+) \((\w+)\) (\d+) (\w+) (\d+) (\d+) (\w+) @(\d+\.\d+)LAST=(\d+\.\d+) BID=(\d+\.\d+) ASK=(\d+\.\d+) MARK=(\d+\.\d+) CLOSE=(\w+) , ACCOUNT (\*{5}\w+)'
    match = re.match(pattern, message)
    extractedOrder = OrderDetail()

    if match != None:
        extractedOrder.OrderId     =   match.group(1)
        extractedOrder.Action      =   match.group(2)
        extractedOrder.Quantity    =   match.group(3)
        extractedOrder.Symbol      =   match.group(4)
        extractedOrder.Shares      =   match.group(5)
        extractedOrder.OptionType  =   match.group(6)
        extractedOrder.Expiry      =   match.group(7) + " " + match.group(8) + " " + match.group(9)
        extractedOrder.Strike      =   match.group(10)
        extractedOrder.ContractType=   match.group(11)
        extractedOrder.ContractPrice=  match.group(12)
        extractedOrder.LastPrice   =   match.group(13)
        extractedOrder.BidPrice    =   match.group(14)
        extractedOrder.AskPrice    =   match.group(15)
        extractedOrder.MarkPrice   =   match.group(16)
        extractedOrder.ClosePrice  =   match.group(17)
        extractedOrder.Account     =   match.group(18)

    extractedOrder.print()

if __name__ == "__main__" :
    message ="#94165383605 BOT +1 NVDA 100 (Weeklys) 28 MAR 25 114 PUT @1.23LAST=115.78 BID=115.77 ASK=115.78 MARK=115.78 CLOSE=null , ACCOUNT *****530SCHW"

    ParseStringByRe(message)