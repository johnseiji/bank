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

def actions(user):
    print('[1] - Depósito\n[2] - Saque\n[3] - Transferência Bancária')
    options = [1, 2, 3]
    act = 0
    while act not in options:
        print('Selecione uma das opções válidas: ')
        act = int(input())
        if act == options[0]:
            print('Opção de depósito selecionada')
            deposit = float(input('Digite a quantia do depósito:\nR$'))
            con = sqlite3.connect('bank.db')
            cur = con.cursor()
            statement = f"SELECT balance from user WHERE email='{user['email']}'"
            cur.execute(statement)
            balance_login = cur.fetchall()
            print(balance_login)
            total = balance_login[0][0] + deposit
            cur.execute("UPDATE user SET balance = ? WHERE email = ?", (total, user['email']))
            con.commit()
            con.close()
            break
'''def deposit_account(id):
    deposit = input('Digite a quantia do depósito:\n ')
    statement = f"SELECT id from user WHERE id='{id}'"
    cur.execute(statement)'''


