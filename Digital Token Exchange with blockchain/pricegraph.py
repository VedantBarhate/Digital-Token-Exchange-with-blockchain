from mysqlessentials import *

class PriceGraph:
    def values(self):
        my_cursor.execute("SELECT * FROM price_graph;")
        value = my_cursor.fetchall()
        return value

    def add_value(self, datetime, price):
        my_cursor.execute(f"INSERT INTO price_graph VALUES ('{datetime}', {price});")
        my_conn.commit()