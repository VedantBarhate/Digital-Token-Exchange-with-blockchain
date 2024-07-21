import mysql.connector

my_conn = mysql.connector.connect(host="localhost", user="root", passwd="@1234", database="digitaltokenexchangewithblockchain")
my_cursor = my_conn.cursor()