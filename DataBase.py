#from curses import noecho
import os, psycopg2, time, logging
from tkinter.tix import Select
from pickle import FALSE
import uuid
from sqlite3 import Row, connect
from dotenv import load_dotenv
from requests import delete

load_dotenv()

class dataBase:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(os.environ['DATABASE_URL'])


    def create_account(self, username, balance):
        with self.conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS accounts (id STRING PRIMARY KEY, balance INT, portfolio_value INT)"
            )
            cur.execute(
                "UPSERT INTO accounts (id, balance, portfolio_value) VALUES (%s, %s, 0)", (username, balance))
            logging.debug("create_accounts(): status message: %s", cur.statusmessage)
        self.conn.commit()


    # this method is called when a user makes a transaction (buy/sell)
    # amount should be negative for sell
    def transaction(self, username, amount):
        with self.conn.cursor() as cur:

            # Check the current balance.
            cur.execute("SELECT balance FROM accounts WHERE id = %s", (username,))
            from_balance = cur.fetchone()[0]
            if from_balance < amount:
                raise RuntimeError(
                    f"insufficient funds in {username}: have {from_balance}, need {amount}"
                )

            # transaction.
            cur.execute(
                "UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, username)
            )

        self.conn.commit()
        logging.debug("transfer_funds(): status message: %s", cur.statusmessage)


    # this method adds a new stock to the table
    def add_stock(self, uuid, stock, amount,) -> None:
        with self.conn.cursor() as cur:
            # todo - maybe use gen_random_uuid()
            # sql = "CREATE TABLE IF NOT EXISTS shares (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), userID UUID REFERENCES accounts, name STRING, amount FLOAT)"
            # print(sql)
            cur.execute(
                "CREATE TABLE IF NOT EXISTS shares (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), userID UUID REFERENCES accounts, name STRING, amount FLOAT)"
            )
            self.conn.commit()
            
            cur.execute(
                'SELECT 1 FROM shares WHERE userid = %s AND name = %s', (uuid, stock)
            )

            # print('fetch-', cur.fetchone())
            if(cur.fetchone() is not None):
                # print("in here")
                cur.execute(
                    'UPDATE shares SET amount = amount + %s WHERE userID = %s AND name = %s', (amount, uuid, stock)
                )
            else:
                cur.execute(
                    'UPSERT INTO shares (userID, name, amount) VALUES (%s, %s, %s)' , (uuid, stock, amount)
                )
            logging.debug("add_stock(): status message: %s", cur.statusmessage) 
        self.conn.commit()


    # returns the balance of the input user
    def getBalance(self, uuid):
        balance = 0
        with self.conn.cursor() as cur:
            cur.execute(
               'SELECT balance FROM accounts WHERE id = %s', (uuid,)
            )
            balance = cur.fetchone()
        
        self.conn.commit()

        return balance


    # return true or false if the user is in the database
    def hasUser(self, discordID):
        with self.conn.cursor() as cur:
            cur.execute(
                'SELECT 1 FROM accounts WHERE id = %s', (discordID,)
            )
            if cur.fetchone() is None:
                return False
        return True


    # this method removes a stock from the table
    def remove_stock(self, uuid, stock, amount) -> None:
        
        with self.conn.cursor() as cur:
            cur.execute(
                'SELECT 1 FROM shares WHERE userid = %s AND name = %s', (uuid, stock)
            )

            if(cur.fetchone() is not None):
                # print("in here")
                cur.execute(
                    'UPDATE shares SET amount = amount - %s WHERE userID = %s AND name = %s', (amount, uuid, stock)
                )

        self.conn.commit()


    def getShareID(self, discordID):
        with self.conn.cursor() as cur:
            cur.execute(
                'SELECT Id from shares WHERE userID = %s', (discordID,)
            )
            # print(cur.fetchall())

            row = cur.fetchone()

            for row in row:
                print(row)

        self.conn.commit()


    def getStockAmount():
        pass


    def getProfolio(self, userID):
        with self.conn.cursor() as cur:
            cur.execute(
                'SELECT name, amount from shares WHERE userID = %s', (userID,)
            )
            # print(cur.fetchall())

            ans = cur.fetchall()

        self.conn.commit()

        return ans




    # tester methods
    def print_balances(self) -> None:
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, balance FROM accounts")
            # logging.debug("print_balances(): status message: %s", cur.statusmessage)
            rows = cur.fetchall()
            self.conn.commit()
            print(f"Balances at {time.asctime()}:")
            for row in rows:
                print(row)
    
    def print_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")

            for table in cur.fetchall():
                print(table)

    def col_names(self, table):
        with self.conn.cursor() as curs:
            curs.execute("Select * FROM %s LIMIT 0" % table)   
            colnames = [desc[0] for desc in curs.description]

        print(colnames)
    
    def print_stock(self, stock) -> None:
        with self.conn.cursor() as cur:
            # cur.execute("SELECT id, %s FROM shares" % stock)
            cur.execute("SELECT id, name FROM shares")
            # logging.debug("print_balances(): status message: %s", cur.statusmessage)
            rows = cur.fetchall()
            self.conn.commit()
            print(f"Stocks at {time.asctime()}:")
            for row in rows:
                print(row)


    def delete_accounts(self) -> None:
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM defaultdb.accounts")
            logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
        self.conn.commit()


    def delete_cols(self, col) -> None:
        with self.conn.cursor() as cur:
            sql = "ALTER TABLE accounts DROP IF EXISTS %s" % col
            cur.execute(sql)
        
        self.conn.commit()


    def delete_table(self) -> None:
        with self.conn.cursor() as cur:
            sql = "DROP TABLE shares"
            cur.execute(sql)
            sql = "DROP TABLE accounts"
            cur.execute(sql)

        self.conn.commit()

    def stockAmount(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT ID, userID, name, amount FROM shares")

            rows = cur.fetchall()
            self.conn.commit()
            print(f"Balances at {time.asctime()}:")
            for row in rows:
                print(row)

        self.conn.commit()





def main():
    portfolio = dataBase()
    # portfolio.delete_table()

    # exit()

    uuid = "acde070d-8c4c-4f0d-9d8a-162843c10333"
    uuid_notExists = "acde070d-8c7c-4f0d-9d8a-162843c10333"

    portfolio.create_account(uuid, 100000)
    a = portfolio.getBalance(uuid)
    print(a)
    # portfolio.print_balances()
    portfolio.transaction(uuid, -55000)
    # portfolio.print_balances()
    a = portfolio.getBalance(uuid)
    print(a)

    # if portfolio.hasUser(uuid_notExists) == False:
    #     print("user doesn't exist")

    # portfolio.getShareID(uuid)

    # portfolio.add_stock(uuid, 'appl', 100)
    # portfolio.stockAmount()


    # portfolio.add_stock(uuid, 'tsla', 15)
    # portfolio.stockAmount()
    
    port = portfolio.getProfolio(uuid)

    print(port)

    # portfolio.col_names("accounts")
    # portfolio.col_names("shares")

    # portfolio.print_stock("APPL")
    
    # portfolio.delete_accounts()
    # portfolio.col_names()
    # portfolio.delete_cols("tsla")
    # portfolio.delete_cols("appl")
    # portfolio.delete_cols("aapl")
    # portfolio.col_names()



if __name__ == "__main__":
    main()