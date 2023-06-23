import random
import matplotlib.pyplot as plt

class Chain:
    def __init__(self):
        self.blockList = list()
        # opcje na ktore mozna oddac glos
        self.optionsList = ["Opcja1", "Opcja2", "Opcja3"]
        self.result = ''

    # zwroc skrot z naglowka ostatniego bloku z lancucha
    def getLastBlockHash(self):
        l = len(self.blockList)
        if l == 0:
            return -1

        return self.blockList[l-1].getHash()

    # dodaj blok do lancucha
    def addBlock(self, block):
        self.blockList.append(block)


    # przeprowadz glosowanie
    def runVoting(self, participants):

        votsPerBlock = 50 # Liczba glosow na blok
        committee_size = 20  # Liczba osob weryfikujacych transakcje w bloku

        # co 50 glosow
        for i in range(0, len(participants), votsPerBlock):
            print("=============================")
            print("Tworzenie nowego bloku")
            print("Wybieranie autora bloku")
            creator = random.choice(participants) # wybierz losowego autora bloku
            voteList = list() # zainicjalizowanie listy glosow


            print("Glosujacy oddaja swoje glosy")
            # przeprowadz glosowanie dla wybranej liczby glosujacych
            for j in range(i, i+votsPerBlock):
                p = participants[j]
                # dokonaj glosowania
                voteList.append(p.vote(random.randint(0, 2)))

            # utworz blok
            print("Tworzenie bloku przez autora")
            block = creator.createBlock(voteList)

            # sprawdz poprwanosc transakcji w bloku
            validators = random.sample(participants, committee_size)
            votesForAdding = 0
            print("Sprawdzanie poprawnosci glosow przez losowo wybranych uczestnikow")
            for validator in validators:
                # w tej uproszczonej wersji mechanizmu zgody zakladam, ze nie wiecej niz 30% glosow moze zostac uznanych za niepoprawne
                if(validator.validateVotes(block.getData(), participants) < (.3 * votsPerBlock)):
                    votesForAdding += 1

            # jezeli walidacja jest poprawna to dodaj blok do lancucha. Komisja musi zgadzac sie co do
            # poprawnosci bloku w co najmniej 80%
            if(votesForAdding > (.8 * committee_size)):
                lbh = self.getLastBlockHash()
                block.setHashToLast(lbh)
                self.blockList.append(block)

                print("Dodano nowy blok")
            else:
                print("Blok zostal odrzucony")

    def calculateResoults(self):
        result = [0,0,0]
        for block in self.blockList:
            blockResult = block.countVotes()
            for i in range(3):
                result[i] += blockResult[i]


        winner = result.index(max(result))
        self.result = self.optionsList[winner]
        print("Wyniki glosowania:", result)
        print("Wygrany to:", self.result)

        plt.pie(result, labels=self.optionsList, autopct='%1.1f%%')
        plt.title('Wyniki glosowania')
        plt.show()

    def validateBlock(self):
        self.blockList[0].verifyMerkleRoot()


