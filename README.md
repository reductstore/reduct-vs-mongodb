# Benchmarks for MongoDB and ReductStore in Python

This repository contains a simple benchmark for MongoDB and ReductStore in Python. The benchmark consists of inserting
binary data into respective databases and measuring the time taken to insert and retrieve the data.

## Running

```bash
pip install -r requirements.txt
docker-compose up -d
python main.py
```

## Results

The following table shows the average time taken to insert and retrieve binary data of different sizes into MongoDB and
ReductStore.

| Chunk Size | Operation | MongoDB, blob/s | ReductStore, blob/s | ReductStore, % |
|------------|-----------|-----------------|---------------------|----------------|
| 10 KB      | Write     | 529             | 1531                | +190%          |
|            | Read      | 379             | 1303                | +244%          |
| 100 KB     | Write     | 542             | 1384                | +155%          |
|            | Read      | 380             | 1131                | +198%          |
| 1 MB       | Write     | 224             | 531                 | +137%          |
|            | Read      | 169             | 358                 | +112%          |
| 10 MB      | Write     | 31              | 80                  | +158%          |
|            | Read      | 23              | 38                  | +65%           |

## Ressources

- [MongoDB](https://www.mongodb.com/)
- [MongoDB Time Series Manual](https://www.mongodb.com/docs/manual/core/timeseries/timeseries-procedures/)
- [MongoDB Large Objects](https://www.mongodb.com/developer/products/mongodb/storing-large-objects-and-files/)
- [ReductStore](https://www.reduct.store/)