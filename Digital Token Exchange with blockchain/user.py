from mysqlessentials import *
import datetime
from blockchain import calculate_hash

def balance_input():
    add = input("Enter amount or 'X' to cancel: ")
    try:
        if add=='X' or add=='x':
            print("Procedure Canceled on request!!")
        else:
            add = int(add)
            return add
    except:
        print("Invalid entry!!...Plz. Try Again!!")
        balance_input()

def buy_sell_input(x):
    try:
        t = int(input(f"Enter how many token you want to {x} (Enter 0 if dont)\n> "))
        return t
    except:
        print("Invalid entry...try again...")
        buy_sell_input(x)

def build_acko(from_, to, n, amnt):
    time=str(datetime.datetime.now())
    time=time.replace(' ', '_')
    transaction_aco = f"{from_}_{to}_{n}_{amnt}_{time}&"
    return transaction_aco

def yes_no_input():
    validation = input("Verify yes/no: ")
    if validation.lower() == 'yes':
        return True
    elif validation.lower() == 'no':
        return False
    else:
        print("Invalid Entry...Try Agian...")
        yes_no_input()

def sender_update(tok_updt, trans_updt, email, price):
    my_cursor.execute(f"UPDATE users SET Tokens={tok_updt}, Transactions='{trans_updt}', Personal_Cap=Tokens*{price} WHERE Email='{email}';")
    my_conn.commit()

def receiver_update(to, trans_aco, tok_send, price):
    my_cursor.execute(f"SELECT Transactions FROM users WHERE Account_no={to};")
    recvr_trans = my_cursor.fetchall()[0][0]
    recvr_trans_updt = recvr_trans+trans_aco
    my_cursor.execute(f"UPDATE users SET Tokens=Tokens+{tok_send}, Transactions='{recvr_trans_updt}', Personal_Cap=Tokens*{price} WHERE Account_no={to};")
    my_conn.commit()

class User:
    def __init__(self, user_data):
        self.user_id = user_data[0]
        self.user_name = user_data[1]
        self.email = user_data[2]
        self.pswd = user_data[3]
        self.acc_no = user_data[4]
        self.trans_key = user_data[5]
        self.balance = user_data[6]
        self.tokens = user_data[7]
        self.blocks_mined = user_data[8]
        self.reward_tokens = user_data[9]
        self.transactions = user_data[10]
        self.personal_cap = user_data[11]

    def profile(self):
        print("@Profile")
        print("User Id: ", self.user_id)
        print("Name: ", self.user_name)
        print("Email: ", self.email)
        print("Account No.: ", self.acc_no)
        print("Balance: ", self.balance)
        print("Tokens: ", self.tokens)
        print("Blocks Mined: ", self.blocks_mined)
        print("Reward Tokens: ", self.reward_tokens)
        print("Personal Cap: ", self.personal_cap)

    def buy(self, tok_fun, price_graph, tok_transactions):
        av_tok = tok_fun.available_tokens()
        tok_pr = tok_fun.price()
        tok_cap = tok_fun.capital()
        total_tok = tok_fun.total_tokens()
        print("@Buying Tokens")
        print(f"You currently own {self.tokens} tokens...")
        print(f"There are currently {av_tok} tokens available to buy...")
        print(f"There are ₹{self.balance} balance in you account...")
        print(f"Current price to Buy Token is ₹{tok_pr} ...")
        tok_buy = buy_sell_input('buy')
        try:
            if tok_buy == 0:
                print("Moving Back...")
            else:
                if tok_buy<av_tok:
                    if tok_buy*tok_pr<=self.balance:
                        t_key = input("Enter your Transaction Key: ")
                        try:
                            if t_key==self.trans_key:
                                trans_aco = build_acko('BROKER', self.acc_no, tok_buy, tok_buy*tok_pr)
                                cap_updt = tok_cap+float(tok_buy*tok_pr)
                                av_tok_updt = av_tok-tok_buy
                                price_updt = float(cap_updt/total_tok)
                                m_cap_updt = price_updt*total_tok
                                bal_updt = self.balance-(tok_buy*tok_pr)
                                tok_updt = self.tokens+tok_buy
                                trans_updt = self.transactions+trans_aco
                                personal_cap_updt = tok_updt*price_updt
                                tok_fun.update_fundamentals(cap_updt, av_tok_updt, price_updt, m_cap_updt)
                                price_graph.add_value(datetime.datetime.now(), price_updt)
                                self.user_update(bal_updt, tok_updt, trans_updt, personal_cap_updt)
                                tok_transactions.add_transaction('BROKER', self.acc_no, tok_buy, tok_buy*tok_pr, datetime.datetime.now())
                                print(tok_buy, "tokens successfully bought!!!")
                            else:
                                print("Unable to verify...try again...")
                                self.buy(tok_fun, price_graph, tok_transactions)
                        except Exception as e:
                                print(e)
                                print("Something went wrong...order not executed...")
                                my_conn.rollback()
                    else:
                        print("Insufficient balance...")
                        self.buy(tok_fun, price_graph, tok_transactions)
                else:
                    print("That much tokens are not available...")
                    self.buy(tok_fun, price_graph, tok_transactions)
        except:
            print("Something went wrong...redirecting to @Buying Tokens!!")
            self.buy(tok_fun, price_graph, tok_transactions)

    def send(self, tok_fun, tok_transactions):
        user_tok = self.tokens
        tok_pr = tok_fun.price()
        print("@Send Tokens")
        print(f"You currently own {self.tokens} tokens...")
        tok_send = buy_sell_input('send')
        try:
            if tok_send == 0:
                print("Moving Back...")
            else:
                if tok_send<=user_tok:
                    to = int(input("Enter Account no. of receiver: "))
                    try:
                        my_cursor.execute(f"SELECT Name FROM users WHERE Account_no={to}")
                        extract_name = my_cursor.fetchall()[0][0]
                        print(f"Sending tokens to: {extract_name}")
                        validation = yes_no_input()
                        if validation:
                            t_key = input("Enter your Transaction Key: ")
                            try:
                                if t_key==self.trans_key:
                                    trans_aco = build_acko(self.acc_no, to, tok_send, tok_send*tok_pr)
                                    tok_updt = self.tokens-tok_send
                                    trans_updt = self.transactions+trans_aco
                                    sender_update(tok_updt, trans_updt, self.email, tok_pr)
                                    receiver_update(to, trans_aco, tok_send, tok_pr)
                                    tok_transactions.add_transaction(self.acc_no, to, tok_send, tok_send*tok_pr, datetime.datetime.now())
                                    print(tok_send," tokens successfully sent to ", to)
                            except:
                                print("Something went wrong...order not executed...")
                                my_conn.rollback()
                        else:
                            print("Order Canceled on request...no tokens were sent...")
                    except:
                        print("Receiver not found...try again")
                        self.send(tok_fun, tok_transactions)
                else:
                    print("That much tokens are not available with you...")
                    self.send(tok_fun, tok_transactions)
        except:
            print("Something went wrong...redirecting to @Send Tokens!!")
            self.send(tok_fun, tok_transactions)

    def sell(self, tok_fun, price_graph, tok_transactions):
        tok_pr = tok_fun.price()
        user_tok = self.tokens
        tok_cap = tok_fun.capital()
        av_tok = tok_fun.available_tokens()
        total_tok = tok_fun.total_tokens()
        print("@Selling Tokens")
        print(f"You currently own {self.tokens} tokens...")
        print(f"Current price to Sell Token is ₹{tok_pr} ...")
        tok_sell = buy_sell_input('sell')
        try:
            if tok_sell == 0:
                print("Moving Back...")
            else:
                if tok_sell<=user_tok:
                    t_key = input("Enter your Transaction Key: ")
                    try:
                        if t_key==self.trans_key:
                            trans_aco = build_acko(self.acc_no, 'BROKER', tok_sell, tok_sell*tok_pr)
                            cap_updt = tok_cap-float(tok_sell*tok_pr)
                            av_tok_updt = av_tok+tok_sell
                            price_updt = float(cap_updt/total_tok)
                            m_cap_updt = price_updt*total_tok
                            bal_updt = self.balance+(tok_sell*tok_pr)
                            tok_updt = self.tokens-tok_sell
                            trans_updt = self.transactions+trans_aco
                            personal_cap_updt = tok_updt*price_updt
                            tok_fun.update_fundamentals(cap_updt, av_tok_updt, price_updt, m_cap_updt)
                            price_graph.add_value(datetime.datetime.now(), price_updt)
                            self.user_update(bal_updt, tok_updt, trans_updt, personal_cap_updt)
                            tok_transactions.add_transaction(self.acc_no, 'BROKER', tok_sell, tok_sell*tok_pr, datetime.datetime.now())
                            print(tok_sell, "tokens successfully sold!!!")
                            print('₹', tok_sell*tok_pr, "added to your balance!!")
                        else:
                            print("Unable to verify...try again...")
                            self.sell(tok_fun, price_graph, tok_transactions)
                    except:
                        print("Something went wrong...order not executed...")
                        my_conn.rollback()
                else:
                    print("That much tokens are not available with you...")
                    self.sell(tok_fun, price_graph, tok_transactions)
        except:
            print("Something went wrong...redirecting to @Selling Tokens!!")
            self.sell(tok_fun, price_graph, tok_transactions)

    def mine_block(self, blockchain, Block, tok_transactions, tok_fun):
        tok_pr = tok_fun.price()
        previous_block_data = blockchain.previous_block_data()
        previous_block_data = str(previous_block_data).split("&")
        transactions = tok_transactions.get_transactions()
        if transactions == []:
            print("Nothing to mine...reverting...")
        else:
            print("Started mining...")
            index = int(previous_block_data[0]) + 1
            timestamp = datetime.datetime.now()
            nonce = 0
            hash = calculate_hash(index, previous_block_data[4], timestamp, transactions, nonce)
            trans_str = ""
            for i in transactions:
                for j in i:
                    trans_str+=str(j)+"_"
                trans_str+="&"
            new_block = Block(index, previous_block_data[4], timestamp, trans_str, hash, nonce)
            info=str(new_block.index)+"&"+str(new_block.previous_hash)+"&"+str(new_block.timestamp)+"&"+str(new_block.transactions)+"&"+str(new_block.hash)+"&"+str(new_block.nonce)
            while not new_block.hash.startswith("0000"):
                new_block.nonce += 1
                new_block.hash = calculate_hash(new_block.index, new_block.previous_hash, new_block.timestamp, new_block.transactions, new_block.nonce)
            print("Mining done...")
            check_transactions = tok_transactions.get_transactions()
            if check_transactions != transactions:
                print("Someone added block before you...no reward for you...")
            else:
                print("Adding block to blockchain...")
                blockchain.add_to_chain(new_block, info,  self.acc_no, timestamp)
                print("Block added to blockchain...")
                my_cursor.execute("UPDATE transactions SET in_block='True' WHERE in_block='False';")
                reward=50
                tok_updt=self.tokens+reward
                reward_tok_updt = self.reward_tokens+reward
                block_mined_updt = self.blocks_mined+1
                per_cap_updt = tok_updt*tok_pr
                trans_aco = build_acko('REWARD', self.acc_no, reward, reward*tok_pr)
                trans_updt = self.transactions+trans_aco
                my_cursor.execute(f"UPDATE users SET Tokens={tok_updt}, Blocks_Mined={block_mined_updt}, Reward_tokens={reward_tok_updt}, Transactions='{trans_updt}', Personal_Cap={per_cap_updt} WHERE email='{self.email}';")
                tok_transactions.add_transaction('REWARD', self.acc_no, reward, reward*tok_pr, datetime.datetime.now())
                my_conn.commit()
                print("You are rewarded with 50 tokens...")

    def show_transactions(self):
        lst = str(self.transactions).split('&')
        lst=lst[0:len(lst)]
        for i in range(1, len(lst)):
            data = lst[i-1]
            data = str(data).split('_')
            print("Transaction no.", i)
            print(" From: ", data[0])
            print(" To:", data[1])
            print(" Tokens:", data[2])
            print(" Amount:", data[3])
            print(" Date:", data[4])
            print(" Time:", data[5])

    def add_balance(self):
        print("@Add Balance")
        print("Your existing balance: ₹", self.balance)
        add = balance_input()
        print(add)
        balance_updt = self.balance + add
        my_cursor.execute(f"UPDATE users SET Balance={balance_updt} WHERE Email='{self.email}';")
        my_conn.commit()

    def updated_user(self):
        my_cursor.execute(f"SELECT * FROM users WHERE Email='{self.email}';")
        user_data = my_cursor.fetchall()
        user = User(user_data[0])
        return user
    
    def user_update(self, balance, tok, trans, personal_cap):
        my_cursor.execute(f"UPDATE users SET Balance={balance}, Tokens={tok}, Transactions='{trans}', Personal_Cap={personal_cap} WHERE Email='{self.email}';")
        my_conn.commit()