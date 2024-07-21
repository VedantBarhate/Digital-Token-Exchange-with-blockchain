from mysqlessentials import *

class Transactions:
    def get_transactions(self):
        my_cursor.execute("SELECT * FROM transactions WHERE in_block='False';")
        result = my_cursor.fetchall()
        return result

    def add_transaction(self, from_, to_, n , amnt, time):
        my_cursor.execute(f"INSERT INTO transactions VALUES ('{from_}', '{to_}', {n}, {amnt}, '{time}', 'False');")
        my_conn.commit()