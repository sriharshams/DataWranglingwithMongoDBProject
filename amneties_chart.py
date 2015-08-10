#!/usr/bin/env python
__author__ = 'sms'
from ggplot import *
import pandas as pd
import pylab
import matplotlib.pyplot as plt

def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client['osm']
    return db


def range_query():
    # You can use datetime(year, month, day) to specify date in the query
    query = [{"$match":{"amenity":{"$exists":1}}}, {"$group":{"_id":"$amenity", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":10}]
    return query

def aggregate(collection, pipeline):
    result = list(collection.aggregate(pipeline))
    return result



if __name__ == "__main__":

    db = get_db()
    collection = db['san_francisco_metro']
    query = range_query()
    amneties = aggregate(collection,query)
    print "Amneties in San Francisco Metro"
    import pprint
    pprint.pprint(amneties)
    x_amnety_list = []
    y_amnety_count = []
    for amnety in amneties:
        x_amnety_list.append(amnety['_id'])
        y_amnety_count.append(amnety['count'])

    df = pd.DataFrame({"x":x_amnety_list, "y":y_amnety_count})
    fig, ax = plt.subplots(figsize=(12, 7))
    df.plot(ax=ax, kind="bar")
    ax.set_title("San Francisco's Metro Amenities")
    ax.set_ylabel("Number of Amenities")
    ax.set_xticklabels(x_amnety_list,
                   rotation=360)
    ax.set_xlabel("Amenities")
    plt.show()


