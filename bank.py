import sqlite3
from utils import create_tables, create_account, login_account, deposit, withdraw

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
                print('[1] - Depósito\n[2] - Saque\n[3] - Transferência Bancária')
                options = [1, 2, 3]
                act = 0
                while act not in options:
                        print('Selecione uma das opções válidas: ')
                        act = int(input())
                        if act == options[0]:
                            deposit(user)
                            break
                        elif act == options[1]:
                            withdraw(user)
                        elif act == options[2]:
                            print('Opção de Transferência Bancária selecionada')



main()
