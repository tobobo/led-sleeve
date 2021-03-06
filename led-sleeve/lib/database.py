import os
import json
import sqlite3

this_dir = os.path.dirname(os.path.realpath(__file__))


class Database:
    def __init__(self, database=f'{this_dir}/../data/database.db'):
        self.conn = sqlite3.connect(database)

    def deserialize_account(self, account):
        provider, id, credentials, sort_order = account
        return {
            'provider': provider,
            'id': id,
            'credentials': json.loads(credentials),
            'sort_order': sort_order
        }

    def update_account_credentials(self, account_id, credentials):
        self.conn.cursor().execute(
            'UPDATE ACCOUNTS SET credentials=? where id=?', (
                credentials, account_id)
        )

    def get_accounts(self):
        rows = self.conn.cursor().execute(
            'SELECT provider, id, credentials, sort_order FROM accounts ORDER BY sort_order ASC').fetchall()
        return map(self.deserialize_account, rows)

    def add_account(self, account):
        try:
            self.conn.cursor().execute(
                'INSERT INTO accounts (provider, id, credentials, sort_order) VALUES (?, ?, ?, (SELECT IFNULL(MAX(sort_order) + 1, 0) FROM accounts))',
                (account['provider'], account['id'],
                 json.dumps(account['credentials']))
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            self.conn.rollback()
            raise
