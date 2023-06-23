from Crypto.Hash import SHA256
from user import User
from chain import Chain
from random import randint

if __name__ == '__main__':
    # utworz lancuch
    chain = Chain()

    # miasta z ktorych moga pochodzic glosy
    cities = ['Warszawa','Gdansk', 'Krakow', 'Gdynia']

    # utworz uzytkownikow
    userList = list()
    for i in range(800):
        c = cities[randint(0, 3)]
        userList.append(User(c))

    # przeprowadz glosowanie
    chain.runVoting(userList)
    print("=========================================")
    print("Wyniki glosowania")
    chain.calculateResoults()
    print("=========================================")
    print("Przykladowa weryfikacja poprawnosci transakcji w bloku za pomoca skrotu Merkle'a")
    chain.validateBlock()

