from datetime import datetime

from pymongo import MongoClient
from gridfs import GridFS

import random
import time
import asyncio

from reduct import Client as ReductClient

BLOB_SIZE = 10_000_000
BLOB_COUNT = min(1000, 1_000_000_000 // BLOB_SIZE)

CHUNK = random.randbytes(BLOB_SIZE)

HOST = "localhost"
CONNECTION_MONGODB = f"mongodb://admin:password@{HOST}:27017/benchmark?authSource=admin"
CONNECTION_REDUCT = f"http://{HOST}:8383"


def setup_database():
    with MongoClient(CONNECTION_MONGODB) as client:
        db = client["benchmark"]
        if "data" not in db.list_collection_names():
            db.create_collection("data", timeseries={"timeField": "time"})


def write_to_mongodb():
    setup_database()

    with MongoClient(CONNECTION_MONGODB) as client:
        db = client["benchmark"]
        fs = GridFS(db)
        data = db["data"]
        count = 0
        for _ in range(BLOB_COUNT):
            blob_id = fs.put(CHUNK, filename=f"blob_{datetime.now().timestamp()}")
            data.insert_one({"time": datetime.now(), "blob_id": blob_id})
            count += BLOB_SIZE

    return count


def read_from_mongodb(t1, t2):
    count = 0
    with MongoClient(CONNECTION_MONGODB) as client:
        db = client["benchmark"]
        fs = GridFS(db)
        data = db["data"]
        for rec in data.find(
            {
                "time": {
                    "$gt": datetime.fromtimestamp(t1),
                    "$lt": datetime.fromtimestamp(t2),
                }
            }
        ):
            blob = fs.get(rec["blob_id"]).read()
            count += len(blob)

    return count


async def write_to_reduct():
    async with ReductClient(
        CONNECTION_REDUCT, api_token="reductstore"
    ) as reduct_client:
        count = 0
        bucket = await reduct_client.get_bucket("benchmark")
        for _ in range(BLOB_COUNT):
            await bucket.write("data", CHUNK)
            count += BLOB_SIZE

        return count


async def read_from_reduct(t1, t2):
    async with ReductClient(
        CONNECTION_REDUCT, api_token="reductstore"
    ) as reduct_client:
        count = 0
        bucket = await reduct_client.get_bucket("benchmark")
        async for rec in bucket.query("data", t1, t2, ttl=90):
            count += len(await rec.read_all())

        return count


if __name__ == "__main__":
    print(f"Chunk size={BLOB_SIZE / 1000_000} Mb, count={BLOB_COUNT}")
    ts = time.time()
    size = write_to_mongodb()
    print(
        f"Write {size / 1000_000} Mb to MongoDB: {BLOB_COUNT / (time.time() - ts)} req/s"
    )

    ts_read = time.time()
    size = read_from_mongodb(ts, time.time())
    print(
        f"Read {size / 1000_000} Mb from MongoDB: {BLOB_COUNT / (time.time() - ts)} req/s"
    )

    loop = asyncio.new_event_loop()
    ts = time.time()
    size = loop.run_until_complete(write_to_reduct())
    print(
        f"Write {size / 1000_000} Mb to ReductStore: {BLOB_COUNT / (time.time() - ts)} req/s"
    )

    ts_read = time.time()
    size = loop.run_until_complete(read_from_reduct(ts, time.time()))
    print(
        f"Read {size / 1000_000} Mb from ReductStore: {BLOB_COUNT / (time.time() - ts)} req/s"
    )
