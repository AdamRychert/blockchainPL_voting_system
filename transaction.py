from Crypto.Hash import SHA256

# w kontekście tego programu transakcje to ,,glosy''

class Transaction:
    def __init__(self, vouterId, decision, signature):
        data = str(vouterId) + ',' + str(decision) + ',' + str(signature)
        # stworz skrot z calosci danych transakcji
        hash = SHA256.new(data.encode('utf-8'))

        self.vouterId = vouterId
        self.decision = decision
        self.signature = signature
        self.hash = hash.hexdigest()