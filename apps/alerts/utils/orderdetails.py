
# Order class
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
        print("----------------------------------------\n")
