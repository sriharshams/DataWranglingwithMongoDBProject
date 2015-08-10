db.san_francisco_metro.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, {"$sort":{"count":­1}}, {"$limit":1}])

db.san_francisco_metro.aggregate([{"$group": {"_id":"$created.user", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":1}])


> db.san_francisco_metro.aggregate([{"$group": {"_id":"$created.user", "count":{
"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":1}])
{ "_id" : "ediyes", "count" : 711152 }


db.char.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, {"$group":{"_id":"$count", "num_users":{"$sum":1}}}, {"$sort":{"_id":1}}, {"$limit":1}])

db.san_francisco_metro.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, {"$group":{"_id":"$count", "num_users":{"$sum":1}}}, {"$sort":{"_id":1}}, {"$limit":1}])

db.char.aggregate([{"$match":{"address.postcode":{"$exists":1}}}, {"$group":{"_id":"$address.postcode", "count":{"$sum":1}}}, {"$sort":{"count":­1}}])

db.san_francisco_metro.aggregate([{"$match":{"address.postcode":{"$exists":1}}}, {"$group":{"_id":"$address.postcode", "count":{"$sum":1}}}, {"$sort":{"count":-1}}])


db.char.aggregate([{"$match":{"address.city":{"$exists":1}}}, {"$group":{"_id":"$address.city", "count":{"$sum":1}}}, {"$sort":{"count":­1}}])

db.san_francisco_metro.aggregate([{"$match":{"address.city":{"$exists":1}}}, {"$group":{"_id":"$address.city", "count":{"$sum":1}}}, {"$sort":{"count":-1}}])

db.char.aggregate([{"$match":{"amenity":{"$exists":1}}}, {"$group":{"_id":"$amenity","count":{"$sum":1}}}, {"$sort":{"count":­1}}, {"$limit":10}])

db.san_francisco_metro.aggregate([{"$match":{"amenity":{"$exists":1}}}, {"$group":{"_id":"$amenity", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":10}])

db.char.aggregate([{"$match":{"amenity":{"$exists":1}, "amenity":"place_of_worship"}},{"$group":{"_id":"$religion", "count":{"$sum":1}}},{"$sort":{"count":­1}}, {"$limit":1}])

db.san_francisco_metro.aggregate([{"$match":{"amenity":{"$exists":1}, "amenity": "place_of_worship"}}, {"$group":{"_id":"$religion", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":1}])


db.san_francisco_metro.aggregate([{"$match":{"amenity":{"$exists":1}, "amenity":"restaurant"}}, {"$group":{"_id":"$cuisine", "count":{"$sum":1}}},        {"$sort":{"count":­1}}, {"$limit":2}])

db.san_francisco_metro.aggregate([{"$match":{"amenity":{"$exists":1}, "amenity": "restaurant"}}, {"$group":{"_id":"$cuisine", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":2}])

db.san_francisco_metro.aggregate([{"$match":{"building":{"$exists":1}}}, {"$group":{"_id":"$building", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":10}])


> db.san_francisco_metro.aggregate([{"$match":{"amenity":{"$exists":1}}}, {"$group":{"_id":"$amenity", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":10}])

> db.san_francisco_metro.aggregate([{"$match":{"amenity":{"$exists":1}}}, {"$group":{"_id":"$amenity", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":10}])