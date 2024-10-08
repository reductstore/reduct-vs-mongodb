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

The following table shows the average time taken to insert and retrieve binary data of different sizes into MongoDB (with GridFS) and
ReductStore.

| Chunk Size | Operation | MongoDB, blob/s | ReductStore, blob/s | ReductStore, % |
|------------|-----------|-----------------|---------------------|----------------|
| 1 KB       | Write     | 799             | 7994                | +900%          |
|            | Read      | 2008            | 47979               | +2300%         |
| 10 KB      | Write     | 783             | 7431                | +850%          |  
|            | Read      | 1918            | 32888               | +1600%         | 
| 100 KB     | Write     | 694             | 3612                | +420%          | 
|            | Read      | 1730            | 6250                | +260%          |
| 1 MB       | Write     | 246             | 663                 | +170%          | 
|            | Read      | 776             | 540                 | -30%           | 

## Ressources

- [MongoDB](https://www.mongodb.com/)
- [MongoDB Time Series Manual](https://www.mongodb.com/docs/manual/core/timeseries/timeseries-procedures/)
- [MongoDB Large Objects](https://www.mongodb.com/developer/products/mongodb/storing-large-objects-and-files/)
- [ReductStore](https://www.reduct.store/)