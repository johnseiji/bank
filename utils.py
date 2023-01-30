import sqlite3

def create_tables():
    con = sqlite3.connect('bank.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS user (id integer primary key autoincrement, name text not null, email text not null, password text not null, balance real not null)")
    con.close()

def create_account():
    print('---------------------------------------------------')
    print('Digite seu nome: ')
    name = input()
    print('Digite seu email: ')
    email = input()
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
        email = input()
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
            print('Login realizado com sucesso')
            print('---------------------------------------------------')
            cur.execute(f"SELECT * FROM user WHERE email='{email}' and password = '{password}'")
            dados = cur.fetchall()
            print(f'Seus dados:\nID: {dados[0][0]}\nUsuário: {dados[0][1]}\nE-mail: {dados[0][2]}\nBalanço Bancário R$:{dados[0][4]}')
            break
    return {'email':dados[0][2], 'balance':dados[0][4]}

def deposit(user):
    print('Opção de depósito selecionada')
    con = sqlite3.connect('bank.db')
    cur = con.cursor()
    statement = f"SELECT balance from user WHERE email='{user['email']}'"
    cur.execute(statement)
    balance = cur.fetchall()
    print(f"Seu saldo atual: R${balance[0][0]}")
    deposit = float(input('Digite a quantia do depósito:\nR$'))
    total = balance[0][0] + deposit
    cur.execute("UPDATE user SET balance = ? WHERE email = ?", (total, user['email']))
    print('Depósito concluído com sucesso')
    print(f'Seu saldo bancário atual: R${total}')
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
    print(f"Seu saldo atual: R${balance[0][0]}")
    withdraw = float(input('Digite a quantia do saque:\nR$'))
    total = balance[0][0] - withdraw
    cur.execute("UPDATE user SET balance = ? WHERE email = ?", (total, user['email']))
    print('Saque concluído com sucesso')
    print(f'Seu saldo bancário atual: R${total}')
    con.commit()
    con.close()


    


