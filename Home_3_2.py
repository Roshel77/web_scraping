from pymongo import DESCENDING, MongoClient


def search_position():
    client = MongoClient('localhost', 27017)
    db = client['positions']
    collection = db.all_positions

    user_price_job = (int(input('Желаемая зп: ')))
    print(list(collection.find({'$or': [{'price_job_min': {'$gte': user_price_job}},
                                        {'price_job_max': {'$gte': user_price_job}}
                                        ]}).sort([("price_job_max", DESCENDING)])))


search_position()