from mysqlessentials import *

class TokenFundamentals:
    def capital(self):
        my_cursor.execute("SELECT Capital FROM token_stats;")
        cap = my_cursor.fetchall()[0][0]
        return cap

    def total_tokens(self):
        my_cursor.execute("SELECT Tokens FROM token_stats;")
        tok = my_cursor.fetchall()[0][0]
        return tok

    def available_tokens(self):
        my_cursor.execute("SELECT Available_Tokens FROM token_stats;")
        av_tok = my_cursor.fetchall()[0][0]
        return av_tok

    def price(self):
        my_cursor.execute("SELECT Price FROM token_stats;")
        price = my_cursor.fetchall()[0][0]
        return price

    def market_cap(self):
        my_cursor.execute("SELECT Market_Cap FROM token_stats;")
        mcap = my_cursor.fetchall()[0][0]
        return mcap

    def last_acc_no(self):
        my_cursor.execute("SELECT last_acc_no FROM token_stats;")
        last_acc_no = my_cursor.fetchall()[0][0]
        return last_acc_no
    
    def update_fundamentals(self, cap, av_tok, price, m_cap):
        my_cursor.execute(f"UPDATE token_stats SET Capital={cap}, Available_tokens={av_tok}, Price={price}, Market_Cap={m_cap};")
        my_cursor.execute(f"UPDATE users SET Personal_Cap=Tokens*{price};")
        my_conn.commit()

    def update_last_acc_no(self, acc_no):
        my_cursor.execute(f"UPDATE token_stats SET last_acc_no={acc_no};")
        my_conn.commit()