# coding:utf-8
"""
@author: weitaochu@gmail.com
@time: 2023/5/21
"""

from typing import (
    NewType,
)

import requests
from loguru import logger

HexStr = NewType('HexStr', str)


class Index:
    client: any
    database: any
    path: any
    first_inscription_height: int
    genesis_block_coinbase_transaction: any
    genesis_block_coinbase_txid: any
    height_limit: any
    options: any
    reorged: bool
    """
    client: Client,
    database: Database,
    path: PathBuf,
    first_inscription_height: u64,
    genesis_block_coinbase_transaction: Transaction,
    genesis_block_coinbase_txid: Txid,
    height_limit: Option<u64>,
    options: Options,
    reorged: AtomicBool,
    """

    def test(self):
        """
        tx.open_table(HEIGHT_TO_BLOCK_HASH)?;
        tx.open_table(INSCRIPTION_ID_TO_INSCRIPTION_ENTRY)?;
        tx.open_table(INSCRIPTION_ID_TO_SATPOINT)?;
        tx.open_table(INSCRIPTION_NUMBER_TO_INSCRIPTION_ID)?;
        tx.open_table(OUTPOINT_TO_VALUE)?;
        tx.open_table(SATPOINT_TO_INSCRIPTION_ID)?;
        tx.open_table(SAT_TO_INSCRIPTION_ID)?;
        tx.open_table(SAT_TO_SATPOINT)?;
        tx.open_table(WRITE_TRANSACTION_STARTING_BLOCK_COUNT_TO_TIMESTAMP)?;

        tx.open_table(STATISTIC_TO_COUNT)?
        """


class Options:
    chain: str

    _first_inscription_height: dict = {
        "mainnet": 767430,
        "regtest": 0,
        "signet": 112402,
        "testnet": 2413343,
    }

    def first_inscription_height(self) -> int:
        return self._first_inscription_height[self.chain]


class RPC:
    endpoint: str
    auth: any

    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def get_transactions(self, txids: []):
        params = []
        for i, txid in enumerate(txids):
            params.append({
                "jsonrpc": "2.0",
                "id": i,
                "method": "getrawtransaction",
                "params": [txid, True]  # True: json, False: hex
            })
        txs = self.batch_call(params)
        # sort by id
        txs = sorted(txs, key=lambda d: d["id"])
        return [tx["result"] for tx in txs]

    def get_block(self, block_hash: HexStr):
        # todo replace 0 to 1 and decode hex data
        return self.call("getblock", [block_hash, 1])  # 1 json, 0 hex

    def get_block_count(self):
        return int(self.call("getblockcount"))

    def get_block_hash(self, height: int = 0):
        return self.call("getblockhash", [height])

    def call(self, method: str, params: [] = None) -> any:
        res = requests.post(
            self.endpoint,
            json={"jsonrpc": "1.0", "id": "ordpy", "method": method, "params": params if params else []}
        )
        return self.response(res)["result"]

    def batch_call(self, data: []) -> []:
        res = requests.post(
            self.endpoint,
            json=data
        )
        return self.response(res)

    @staticmethod
    def response(res):
        try:
            res_json = res.json()
            if isinstance(res_json, dict):
                if res_json.get("error"):
                    raise ValueError(res_json.get("error"))
            return res_json
        except Exception as e:
            raise ValueError(res.content)


class Epoch:
    def __init__(self, height):
        self.height = height

    @staticmethod
    def subsidy(height):
        return 50 * 100_000_000 >> height // 210_000

    @classmethod
    def first_ordinal(cls, height):
        start = 0
        for height in range(height):
            start += cls.subsidy(height)
        return start


class Updater:
    height: int = 1
    rpc: RPC
    index: Index

    def __init__(self, endpoint: str, index: Index = None):
        self.endpoint = endpoint
        self.rpc = RPC(self.endpoint)
        self.index = index

    def update(self):
        pass

    def index_block(self):
        # table OUTPOINT_TO_VALUE
        if self.height >= 767430:
            pass

        # HEIGHT_TO_BLOCK_HASH
        sat_ranges_written = 0
        outputs_in_block = 0
        # time = block["header"]["time"]

    def update_index(self):
        current_height = self.rpc.get_block_count() + 1
        while True:
            block_data = self.fetch_blocks_from(self.height)

            txs = self.rpc.get_transactions(block_data["tx"])

            for tx in txs:
                print(tx["vout"])

            time = block_data["time"]
            logger.info(f"Block {self.height} at {time} with {len(block_data['tx'])} transactions…", )

            # INSCRIPTION_ID_TO_INSCRIPTION_ENTRY

            start_sat = Epoch.first_ordinal(self.height)
            print(start_sat, start_sat+Epoch.subsidy(self.height))


            # batch requests
            batch_size = 10

            self.height += 1
            if self.height >= 3:
                break

    def spawn_fetcher(self):
        pass

    def fetch_blocks_from(self, height: int):
        block_hash = self.rpc.get_block_hash(height)
        return self.rpc.get_block(block_hash)


class InscriptionUpdater:
    pass


if __name__ == '__main__':
    updater = Updater("")
    updater.update_index()
    # print(rpc.get_block_count())
    # print(rpc.get_block_hash(0))
    # print(rpc.get_block("000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"))
