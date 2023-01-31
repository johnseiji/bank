import sqlite3

def create_tables():
    con = sqlite3.connect('bank.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS user (id integer primary key autoincrement, name text not null, email text not null, password text not null, balance real not null)")
    con.close()

def create_account():
    print('---------------------------------------------------')
    print('Digite seu nome: ')
    name = input().strip().capitalize()
    print('Digite seu email: ')
    email = input().strip().lower()
    print('Digite sua senha: ')
    password = input()
    balance = 0
    con = sqlite3.connect('bank.db')
    cur = con.cursor()
    cur.execute("INSERT INTO user(name, email, password, balance) VALUES (?, ?, ?, ?)", (name, email, password, balance))
    con.commit()
    con.close()
    print('---------------------------------------------------')
    print('Conta criada com sucesso')
    print('---------------------------------------------------')
    print('Seus dados')
    print(f'Nome: {name}\nEmail: {email}\nSenha: {password}')

def login_account():
    while True:
        print('Digite o e-mail: ')
        email = input().strip().lower()
        print('Digite a senha: ')
        password = input()
        con = sqlite3.connect('bank.db')
        cur = con.cursor()
        statement = f"SELECT id from user WHERE email='{email}' and password = '{password}'"
        cur.execute(statement)
        if not cur.fetchone():
            print('Falha ao fazer login\nTente novamente')
        else:
            print('---------------------------------------------------')
            print("\033[1;32;40mLogin realizado com sucesso\033[m")
            print('---------------------------------------------------')
            cur.execute(f"SELECT * FROM user WHERE email='{email}' and password = '{password}'")
            dados = cur.fetchall()
            print(f'Seus dados:\nID: {dados[0][0]}\nUsuário: {dados[0][1]}\nE-mail: {dados[0][2]}\nBalanço Bancário R${dados[0][4]}')
            break
    return {'email':dados[0][2], 'balance':dados[0][4], 'name':dados[0][1]}

def deposit(user):
    print('Opção de depósito selecionada')
    con = sqlite3.connect('bank.db')
    cur = con.cursor()
    statement = f"SELECT balance from user WHERE email='{user['email']}'"
    cur.execute(statement)
    balance = cur.fetchall()
    print(f"Seu saldo atual: R${balance[0][0]:.2f}")
    deposit = float(input('Digite a quantia do depósito:\nR$'))
    total = balance[0][0] + deposit
    cur.execute("UPDATE user SET balance = ? WHERE email = ?", (total, user['email']))
    print(f'\033[1;32;40mDepósito de R${deposit:.2f} concluído com sucesso\033[m')
    print(f'Seu saldo bancário atual: R${total:.2f}')
    con.commit()
    con.close()
    return total

def withdraw(user):
    print('Opção de saque selecionada')
    con = sqlite3.connect('bank.db')
    cur = con.cursor()
    statement = f"SELECT balance from user WHERE email='{user['email']}'"
    cur.execute(statement)
    balance = cur.fetchall()
    print(f"Seu saldo atual: R${balance[0][0]:.2f}")
    withdraw = float(input('Digite a quantia do saque:\nR$'))
    if balance[0][0] < withdraw:
        print('Você não possui saldo suficiente para realizar essa operação.')
        con.close()
        return
    total = balance[0][0] - withdraw
    cur.execute("UPDATE user SET balance = ? WHERE email = ?", (total, user['email']))
    print(f'\033[1;32;40mSaque de R${withdraw:.2f} concluído com sucesso\033[m')
    print(f'Seu saldo bancário atual: R${total:.2f}')
    con.commit()
    con.close()
    return total

def transfer(user):
    print('Opção de transferência bancária selecionada')
    con = sqlite3.connect('bank.db')
    cur = con.cursor()
    print(f"O seu saldo atual é {user['balance']}")
    email_transfer = input('Digite o e-mail da conta que receberá a transferência: ').lower().strip()
    statement = f"SELECT balance from user WHERE email='{email_transfer}'"
    cur.execute(statement)
    if not cur.fetchone():
        print('Usuário não encontrado\nTente novamente')
    else:
        value_transfer = float(input('Digite o valor que deseja transferir R$'))
        statement = f"SELECT balance from user WHERE email='{user['email']}'"
        cur.execute(statement)
        user_balance = cur.fetchall()
        if user_balance[0][0] < value_transfer:
            print('Você não possui saldo suficiente para realizar essa operação.')
            con.close()
            return
        new_cur_user_balance = user_balance[0][0] - value_transfer
        cur.execute("UPDATE user SET balance = ? WHERE email = ?", (new_cur_user_balance, user['email']))
        print(f'Seu saldo após a transferência é de R${new_cur_user_balance:.2f}')
        statement = f"SELECT balance from user WHERE email='{email_transfer}'"
        cur.execute(statement)
        transfer_user = cur.fetchall()[0][0]
        total_user_transfer = transfer_user + value_transfer
        cur.execute("UPDATE user SET balance = ? WHERE email = ?", (total_user_transfer, email_transfer))
        print(f'\033[1;32;40mValor de R${value_transfer:.2f} transferido com sucesso para a conta {email_transfer}\033[m')
        con.commit()
        con.close()
        return new_cur_user_balance
