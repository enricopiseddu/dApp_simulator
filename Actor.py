class Actor:
    def __init__(self):
        self.id = ''
        self.nrTx = 0
        self.transactions = []
        self.schedule = ''
        self.nrComplexTx = 0

    def addTransaction(self, aTransaction):
        self.transactions.append(aTransaction)

    def isCustomer(self):
        return False

    def isOperator(self):
        return False
