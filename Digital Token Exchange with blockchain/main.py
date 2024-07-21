from mysqlessentials import *
from user import User
from token_fundamentals import TokenFundamentals
from pricegraph import PriceGraph
from token_transactions import Transactions
import matplotlib.pyplot as plt
from blockchain import Block, Blockchain

def auth_input():
    ch = int(input("> "))
    if ch not in [1,2,3]:
        print("Invalid Input...Try Again!!!")
        auth_input()
    else:
        return ch
    
def check_credentials(email, pswd):
    my_cursor.execute(f"SELECT COUNT(*) FROM users WHERE email='{email}' AND Password='{pswd}';")
    result = my_cursor.fetchall()
    if result[0][0] == 1:
        return True
    else:
        return False

def email_input():
    email = input("Email: ")
    my_cursor.execute(f"SELECT COUNT(*) FROM users WHERE Email='{email}';")
    result = my_cursor.fetchall()
    if result[0][0] > 0:
        print("Email Already in Use...Use Another Email...")
        email_input()
    else:
        return email

def home_input():
    ch = int(input("Enter Your Choice:\n1. See Profile\n2. Buy Tokens\n3. Send Tokens\n4. Sell Tokens\n5. Mine Block\n6. Previous Transcations\n7. See Current Stats for Tokens\n8. Add Balance\n9. See Price Graph\n10. Exit\n> "))
    if ch not in list(range(1,11)):
        print("Invalid Input...Try Again!!!")
        home_input()
    else:
        return ch

def token_stats(tok_fun):
    print("@Token Stats")
    cap = tok_fun.capital()
    total_tok = tok_fun.total_tokens()
    av_tok = tok_fun.available_tokens()
    price = tok_fun.price()
    m_cap = tok_fun.market_cap()
    print("Capital: ", cap)
    print("Total Tokens: ", total_tok)
    print("Available Tokens: ", av_tok)
    print("Price: ₹", price)
    print("Market Cap: ", m_cap)

def get_price_graph(price_graph):
    values = price_graph.values()
    time_values = [coord[0] for coord in values]
    price_values = [coord[1] for coord in values]
    plt.plot(time_values, price_values, marker='o', linestyle='-')
    plt.title('Plot of (DateTime, Price) Coordinates')
    plt.xlabel('Datetime')
    plt.ylabel('Price')
    plt.grid(True)
    plt.show()

class App:
    def __init__(self):
        self.tok_fun = TokenFundamentals()
        self.price_graph = PriceGraph()
        self.tok_transactions = Transactions()
        self.blockchain = Blockchain()
        self.blockchain.create_genesis_block()

    def auth(self):
        print("@Authentication Page")
        print("1. Login\n2. Create Account\n3. Exit")
        ch = auth_input()
        if ch==1:
            self.login()
        elif ch==2:
            self.create_account(self.tok_fun)
        elif ch==3:
            my_conn.close()
            exit()

    def login(self):
        print("@LogIn Page")
        email = input("Enter Email: ")
        pswd = input("Enter Password: ")
        if check_credentials(email, pswd):
            print("Login Successfull!!\n")
            my_cursor.execute(f"SELECT * FROM users WHERE Email='{email}';")
            user_data = my_cursor.fetchall()
            user = User(user_data[0])
            self.home(user)
        else:
            print("LogIn Failed!\nPlz. Try Again!!")
            self.auth()

    def create_account(self, tok_fun):
        print("@Create Account")
        try:
            user_name = input('Name: ')
            email = email_input()
            pswd = input("Password: ")
            last_acc_no = self.tok_fun.last_acc_no()
            acc_no = int(last_acc_no)+1
            trans_key = input("Transaction Key: ")
            balance = float(input("Balance ₹ : "))
            my_cursor.execute(f"INSERT INTO users (Name, Email, Password, Account_no, Transaction_Key, Balance, Tokens, Blocks_mined, Reward_tokens, Transactions, Personal_Cap) VALUES ('{user_name}', '{email}', '{pswd}', {acc_no}, '{trans_key}', '{balance}', 0, 0, 0, '', 0);")
            tok_fun.update_last_acc_no(acc_no)
            my_conn.commit()
            print("Account Successfully Created!...\n")
            self.login()
        except:
            print("You messed up...try again")
            self.auth()

    def home(self, user):
        user=user
        user=user.updated_user()
        while True:
            print("@Home")
            ch = home_input()
            if ch == 1:
                user.profile()
            elif ch == 2:
                user.buy(self.tok_fun, self.price_graph, self.tok_transactions)
            elif ch == 3:
                user.send(self.tok_fun, self.tok_transactions)
            elif ch == 4:
                user.sell(self.tok_fun, self.price_graph, self.tok_transactions)
            elif ch == 5:
                user.mine_block(self.blockchain, Block, self.tok_transactions, self.tok_fun)
            elif ch == 6:
                user.show_transactions()
            elif ch == 7:
                token_stats(self.tok_fun)
            elif ch == 8:
                user.add_balance()
            elif ch == 9:
                get_price_graph(self.price_graph)
            elif ch == 10:
                my_conn.close()
                break
            user=user.updated_user()
            print("\n")

if __name__ == "__main__":
    print("___USELESS TOKEN____\n")
    app = App()
    app.auth()
