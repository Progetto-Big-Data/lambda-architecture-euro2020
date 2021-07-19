from dask.dataframe.core import DataFrame
from dask.distributed import Client
import dask.dataframe as dd
import pymongo

client = Client('tcp://localhost:8786')

fixtures = dd.read_csv('dataset/historical_euro_fixtures/*.csv')

host_counted = fixtures.groupby(['country']).country.count()

host_counted = host_counted.compute()


client = pymongo.MongoClient(
    "localhost",
    27017,
    username="root",
    password="secret")

db = client.batch_view
hosts_collection = db.total_hosts

for nation, hosted in host_counted.items():
    hosts_collection.insert_one({'nation': nation, 'n_hosted': hosted})