import sqlite3
from utils import create_tables, create_account, login_account, actions

def main():
    user = None
    create_tables()
    while True:
        valid_options = [1, 2]
        resp = 0
        while resp not in valid_options:
            print('---------------------------------------------------')
            print('Selecione uma das opções abaixo:\n1 - Entrar\n2 - Criar uma conta')
            resp = int(input())
            if resp == 2:
                create_account()
            elif resp == 1:
                user = login_account()
                print(user)
                actions(user)


main()
