# coding:utf-8
"""
@author: weitaochu@gmail.com
@time: 2023/5/22
"""
import sqlite3


class DB:
    def __init__(self):
        self.db = sqlite3.connect("./test.db")
        self.create_tables()

    def create_tables(self):
        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS sat_index(
                `txid` VARCHAR(46) NOT NULL,
                `start` BIGINT NOT NULL,
                `end` BIGINT NOT NULL,
                `id` INT NOT NULL,
                `height` BIGINT NOT NULL,
                `address` VARCHAR(128) NOT NULL,
                PRIMARY KEY(txid, id, end)
            )
            """
        )

        self.db.commit()

    def insert_sat_index(self, tx_id, start, end, index, height, address):
        self.db.execute(f"""
            INSERT INTO sat_index 
            VALUES ('{tx_id}', {start}, {end}, {index}, {height}, '{address}')
            ON CONFLICT("txid", "id", "end")
            DO UPDATE SET start={start}, end={end}, height={height}
            """)
        self.db.commit()

    def get_sat_index_by_txid_id(self, tx_id, id):
        cur = self.db.cursor()
        cur.execute(f"""
            SELECT * 
            FROM sat_index
            WHERE txid='{tx_id}' and id={id}
            ORDER BY start ASC
        """)
        return cur.fetchall()

    def remove_sat_index(self, tx_id, id, end):
        self.db.execute(f"""
        DELETE from sat_index
        WHERE txid='{tx_id}' and id={id} and end={end}
        """)

    def get_latest_height(self):
        cur = self.db.cursor()
        cur.execute("""
            SELECT height 
            FROM sat_index
            ORDER BY height desc
            limit 1; 
        """)
        one = cur.fetchone()
        return one[0] if one else one
