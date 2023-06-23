from Crypto.Hash import SHA256
from merkleTree import MerkleTree
class Block:
    def __init__(self, voteList, creator):
        # naglowek bloku
        self.hashPointer = {
            "pointer": '',
            "hash": '',
        }
        self.data = voteList # lista glosow
        self.creator = creator # autor bloku

    # zwroc skrot bloku z naglowka
    def getHash(self):
        return self.hashPointer["hash"]
    # zwroc liste glosow
    def getData(self):
        return self.data
    # oblicz korzen/skrot drzewa Merkle'a
    def calculateMerkleRoot(self):
        # utworz liste skrotow transakcji
        transactionHashes = [transaction.hash for transaction in self.data]

        # zbuduj drzewo
        merkleTree = MerkleTree(transactionHashes)

        # otrzymaj skrot drzewa
        merkleRoot = merkleTree.getRootHash()

        print("Skrot drzewa: ", merkleRoot)

        return merkleRoot

    # wpisz dane do naglowka bloku: wskaznik na poprzedni blok, oraz skrot z calosci danych
    def setHashToLast(self, prevBlockHash):
        self.hashPointer["pointer"] = prevBlockHash

        data = str(self.hashPointer["pointer"]) + ',' + str(self.calculateMerkleRoot()) + ',' + self.creator
        hash = SHA256.new(data.encode('utf-8'))
        self.hashPointer["hash"] = hash.hexdigest()

    # weryfikacja poprawnosci transakcji poprzez skrot merkle'a
    def verifyMerkleRoot(self):
        storedHash = self.hashPointer["hash"]

        # oblicz skrot Merklea
        recalculatedMerkleRoot = self.calculateMerkleRoot()

        # polacz dane aby uzyskac skrot jak ten pierwotny
        data = str(self.hashPointer["pointer"]) + ',' + str(recalculatedMerkleRoot) + ',' + self.creator
        finalHash =  SHA256.new(data.encode('utf-8')).hexdigest()

        # porownaj skroty
        if storedHash == finalHash:
            print("Transakcje w bloku sa poprawne")
        else:
            print("Transakcje w bloku byly zmodyfikowane")

    def countVotes(self):
        votesCount = [0,0,0]
        for vote in self.data:
            votesCount[vote.decision] += 1
        return votesCount