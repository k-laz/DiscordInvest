from curses import noecho
import os, psycopg2, time, logging
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
                "UPSERT INTO accounts (id, balance) VALUES ('zdon', 1500)")
            logging.debug("create_accounts(): status message: %s", cur.statusmessage)
        self.conn.commit()


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
    connect = dataBase()

    connect.create_account("zdon", 100000)

    connect.print_balances()
    connect.delete_accounts()
    connect.print_balances()

if __name__ == "__main__":
    main()