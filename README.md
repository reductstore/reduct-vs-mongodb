# Benchmarks for MongoDB and ReductStore in Python

This repository contains a simple benchmark for MongoDB and ReductStore in Python. The benchmark consists of inserting binary data into respective databases and measuring the time taken to insert and retrieve the data.

## Running

```bash
pip install -r requirements.txt
docker-compose up -d
python main.py
```

## Results

The following table shows the average time taken to insert and retrieve binary data of different sizes into MongoDB and ReductStore.

| Chunk Size | Operation | MongoDB, blob/s | ReductStore, blob/s | ReductStore, %  |
|------------|-----------|-----------------|---------------------|-----------------|
| 10 KB      | Write     | 258             | 223                 | -14             |
|            | Read      | 187             | 195                 | 4               |
| 100 KB     | Write     | 145             | 197                 | 36              |
|            | Read      | 108             | 145                 | 34              |
| 1 MB       | Write     | 32              | 52                  | 63              |
|            | Read      | 20              | 29                  | 45              |
| 10 MB      | Write     | 4               | 7                   | 75              |
|            | Read      | 2               | 4                   | 100             |


## Ressources

- [MongoDB](https://www.mongodb.com/)
- [MongoDB Time Series Manual](https://www.mongodb.com/docs/manual/core/timeseries/timeseries-procedures/)
- [MongoDB Large Objects](https://www.mongodb.com/developer/products/mongodb/storing-large-objects-and-files/)
- [ReductStore](https://www.reduct.store/)