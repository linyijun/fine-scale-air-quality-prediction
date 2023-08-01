import pymongo
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


PSQL_CONN_URI = 'postgresql+psycopg2://{usr}:{pwd}@{server}/air_quality_dev' \
    .format(usr='', pwd='')

engine = create_engine(PSQL_CONN_URI, echo=False)

Session = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()

session = Session()


MG_CONN_URI = "mongodb://"


def write_mongodb(t, document, collection_name):

    client = pymongo.MongoClient(MG_CONN_URI)
    db = client['jonsnow']
    collection = db[collection_name]
    condition = {'timestamp': t}
    data = collection.find_one(condition)

    if data is not None:
        collection.update_one(condition, {'$set': document})
        print('Overwrite {}'.format(t))
    else:
        collection.insert_one(document)
        print('Insert {}'.format(t))

    client.close()
