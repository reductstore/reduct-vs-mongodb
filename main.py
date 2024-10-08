import asyncio
import random
import time
from datetime import datetime

from gridfs import GridFS
from pymongo import MongoClient
from reduct import Client as ReductClient, Batch

BLOB_SIZE = 1_000
BLOB_COUNT = min(2000, 10_000_000_000 // BLOB_SIZE)

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
        batch = Batch()
        for _ in range(BLOB_COUNT):
            batch.add(timestamp=datetime.now().timestamp(), data=CHUNK)
            await asyncio.sleep(0.000001)  # To avoid time collisions
            if len(batch) > 80 or batch.size > 8_000_000:
                await bucket.write_batch("data", batch)
                count += batch.size
                batch.clear()

        # Write the last batch
        if len(batch) > 0:
            await bucket.write_batch("data", batch)
            count += batch.size

        return count


async def read_from_reduct(t1, t2):
    async with ReductClient(
        CONNECTION_REDUCT, api_token="reductstore"
    ) as reduct_client:
        count = 0
        bucket = await reduct_client.get_bucket("benchmark")
        async for rec in bucket.query("data", t1, t2):
            async for chunk in rec.read(n=16_000):
                count += len(chunk)

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
        f"Read {size / 1000_000} Mb from MongoDB: {BLOB_COUNT / (time.time() - ts_read)} req/s"
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
        f"Read {size / 1000_000} Mb from ReductStore: {BLOB_COUNT / (time.time() - ts_read)} req/s"
    )