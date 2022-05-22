#from curses import noecho
import os, psycopg2, time, logging
import uuid
from sqlite3 import connect
from dotenv import load_dotenv
from requests import delete

load_dotenv()

class dataBase:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(os.environ['DATABASE_URL'])


    def create_account(self, username, balance):
        with self.conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS accounts (id UUID PRIMARY KEY, balance INT, portfolio_value INT)"
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
            
            # add the column if it does not exists
            # sql = "ALTER TABLE accounts ADD COLUMN IF NOT EXISTS %s INT" % stock

            # todo - maybe use gen_random_uuid()
            sql = "CREATE TABLE IF NOT EXISTS shares (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), userID UUID REFERENCES accounts, name STRING, amount FLOAT)"
            # print(sql)
            cur.execute(
                sql 
            )

            # todo - error here
            sql = "UPSERT INTO shares (id, userID, name, amount) VALUES(gen_random_uuid(), %s, %s, %s)" % (uuid, stock, amount)
            print(sql)
            cur.execute(
                sql
            )

        self.conn.commit()
        logging.debug("add_stock(): status message: %s", cur.statusmessage)
    


    # this method removes a stock from the table
    def remove_stock(self, stock, amount) -> None:
        pass

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
            sql = "DROP TABLE accounts"
            cur.execute(sql)

        self.conn.commit()


def main():
    portfolio = dataBase()
    # portfolio.delete_table()

    uuid = "acde070d-8c4c-4f0d-9d8a-162843c10333"

    portfolio.create_account(uuid, 100000)
    portfolio.print_balances()
    portfolio.transaction(uuid, -55000)
    portfolio.print_balances()

    portfolio.add_stock(uuid, "APPL", 5)

    portfolio.col_names("accounts")
    portfolio.col_names("shares")

    portfolio.print_stock("APPL")
    
    # portfolio.delete_accounts()
    # portfolio.col_names()
    # portfolio.delete_cols("tsla")
    # portfolio.delete_cols("appl")
    # portfolio.delete_cols("aapl")
    # portfolio.col_names()



if __name__ == "__main__":
    main()