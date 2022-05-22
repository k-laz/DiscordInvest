#from curses import noecho
import os, psycopg2, time, logging
from sqlite3 import connect
from dotenv import load_dotenv

load_dotenv()

class dataBase:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(os.environ['DATABASE_URL'])


    def create_account(self, username, balance):
        with self.conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS accounts (id STRING PRIMARY KEY, balance INT)"
            )
            cur.execute(
                "UPSERT INTO accounts (id, balance) VALUES (%s, %s)", (username, balance))
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


    def delete_accounts(self) -> None:
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM defaultdb.accounts")
            logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
        self.conn.commit()



def main():
    portfolio = dataBase()
    portfolio.create_account("zdon", 100000)
    portfolio.print_balances()

    portfolio.transaction("zdon", -55000)
    portfolio.print_balances()
    portfolio.transaction("zdon", 5000)
    portfolio.print_balances()

if __name__ == "__main__":
    main()