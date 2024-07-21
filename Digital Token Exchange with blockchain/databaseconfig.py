import mysql.connector

DB_NAME="digitaltokenexchangewithblockchain"

def mainloop():
    global my_cursor, my_conn
    my_conn = mysql.connector.connect(host="localhost", user="root", passwd="@1234")
    my_cursor = my_conn.cursor()

    my_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")

    my_cursor.execute(f"USE {DB_NAME};")

    my_cursor.execute("""CREATE TABLE IF NOT EXISTS token_stats(
        Capital double,
        Tokens int,
        Available_Tokens int,
        Price double,
        Market_Cap double,
        last_acc_no int);""")
    
    my_cursor.execute("insert into token_stats values(1000000000.0, 1000000000, 1000000000, 1.0, 10000000000.0, 1000000000);")
    
    my_conn.commit()

    my_cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        User_Id int not null auto_increment Primary Key,
        Name varchar(255),
        Email varchar(255),
        Password varchar(255),
        Account_no int,
        Transaction_Key varchar(255),
        Balance double,
        Tokens int,
        Blocks_Mined int,
        Reward_tokens int,
        Transactions longtext,
        Personal_Cap double);""")
    
    my_cursor.execute("""CREATE TABLE IF NOT EXISTS price_graph(
        date_time varchar(255),
        price double);""")
    
    my_cursor.execute("""CREATE TABLE IF NOT EXISTS blockchain_db(
        Block varchar(255),
        Info longtext,
        Mined_by varchar(255),
        Date_time varchar(255));""")
    
    my_cursor.execute("""CREATE TABLE IF NOT EXISTS transactions(
        from_ varchar(255),
        to_ varchar(255),
        n int,
        amount double,
        date_time varchar(255),
        in_block varchar(255));""")

    my_conn.commit()

if __name__ == "__main__":
    mainloop()