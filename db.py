import os
import psycopg2



class DB:
    def __init__(self):
        self.conn = None

    def conn(self):
        # Connect to CockroachDB
        self.conn = psycopg2.connect(os.environ['DATABASE_URL'])
        statements = [
            # CREATE the users table
            "CREATE TABLE IF NOT EXISTS users (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), cash FLOAT)",
            # CREATE the shares table
            "CREATE TABLE IF NOT EXISTS shares (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), userID UUID REFERENCES users, name STRING, amount FLOAT)",
        ]

        for statement in statements:
            self.exec_statement(self.conn, statement)

    def exec_statement(self, conn, stmt):
        try:
            with conn.cursor() as cur:
                cur.execute(stmt)
                row = cur.fetchone()
                conn.commit()
                if row: print(row[0])
        except psycopg2.ProgrammingError:
            return

    def get_user(self, userID):
        statements = [
            # select user
            f'SELECT * FROM users WHERE id = {userID}',
            # CREATE the shares table
            f'SELECT * FROM shares WHERE id = {userID}',
        ]
        for statement in statements:
            self.exec_statement(self.conn, statement)
        

    
    def insert_user(self, userID):
        self.exec_statement(self.conn, f'INSERT INTO users (id, cash) VALUES {userID, 100000}')

    def close(self):
        # Close communication with the database
        self.conn.close()
