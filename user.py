from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Signature import DSS
import secrets
from transaction import Transaction
from block import Block
import random

class User:
    def __init__(self, city):
        key = ECC.generate(curve='P-256')
        self.key = key #klucze uzytkownika
        self.pubKey = key.public_key() #klucz publiczn
        self.id = secrets.token_hex(32) #losowo utworzone id
        self.city = city #miasto

    # akcja glosowania
    def vote(self, decision):
        signature = self.generateSignature(decision) #podpisywanie decyzji
        vote = Transaction(self.id, decision, signature) #tworzenie transakcji/glosu
        return vote

    # akcja podpisu glosu
    def generateSignature(self, decision):
        # Tresc podpisu to id uzytkownika i jego decyzja rozdzielone przecinkiem
        data = str(self.id) + ',' + str(decision)
        # utworzenie skrotu
        hash = SHA256.new(data.encode('utf-8'))

        # podpisanie danych kluczem prywatnym
        signer = DSS.new(self.key, 'fips-186-3')
        signature = signer.sign(hash)

        return signature

    # sprawdzanie poprawnosci podpisu (potrzebne w przypadku gdy uzytkkownik nalezy do komisji sprawdzajacej glosy)
    def validateSignature(self, message, signature, key):
        h = SHA256.new(message.encode('utf-8')) #utworz skrot z tresci wiadomosci
        verifier = DSS.new(key, 'fips-186-3') #utworz obiekt umozliwiajacy weryfikacje an podstawie klucza publicznego
        try:
            # zweryfikuj poprawnosc podpisu
            verifier.verify(h, signature)

            # aby zasymulowac niezgodnosci przyjmiemy 80% szanse na poprawnosc transakcji
            if random.random() > 0.8:
                return False
            return True
        except ValueError:
            return False
    # tworzenie nowego bloku
    def createBlock(self, voteList):
        return Block(voteList, self.id)

    # akcja walidacji glosow w bloku
    def validateVotes(self, voteList, participants):
        numOfInvalid = 0
        for vote in voteList:
            # utworz skrot z danych glosu/transakcji
            data = str(vote.vouterId) + ',' + str(vote.decision) + ',' + str(vote.signature)
            valHash = SHA256.new(data.encode('utf-8')).hexdigest()

            # polacz dane jak w przypadku generowania podpisu (id_uzytkownika,decyzja)
            data = str(vote.vouterId) + ',' + str(vote.decision)
            key = ''
            # zdobadz klucz prywatny uzytkownika, ktory oddal ten glos
            for p in participants:
                if(p.id == vote.vouterId):
                    key = p.pubKey
                    break
            # sprawdzamy czy zgadza sie przekazany skrot z faktycznym skrotem oraz weryfikujemy autora glosu na podstawie jego sygnatury.
            # W prawdziwym zastosowaniu wykorzystany zostalby bardziej zaawansowany algorytm rozwazajacy rozne przypadki.
            if(valHash == vote.hash and self.validateSignature(data, vote.signature, key)):
                continue
            else:
                numOfInvalid += 1

        return numOfInvalid