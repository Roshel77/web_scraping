from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparsPipeline:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.mongo_db = self.client.vacancy

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            salary_list = []
            for i in item['salary']:
                s = i.replace(" ", "").replace("\xa0", "")
                salary_list.append(s)
            # print()
            item['salary'] = salary_list
            if item['salary'][0] == 'от':
                item['salary_min'] = item['salary'][1]
                if item['salary'][2] == 'до':
                    item['salary_max'] = item['salary'][3]
                    item['currency'] = item['salary'][5]
                else:
                    item['salary_max'] = None
                    item['currency'] = item['salary'][3]
                if item['salary'][0] != 'от':
                    item['salary_min'] = item['salary'][0]
                    item['currency'] = item['salary'][3]
            elif item['salary'][0] == 'до':
                item['salary_min'] = None
                item['salary_max'] = int(item['salary'][1])
                item['currency'] = item['salary'][3]
            else:
                item['salary_min'] = None
                item['salary_max'] = None
            # del item['salary']
            item['site'] = 'https://hh.ru'
            collection = self.mongo_db[spider.name]
            collection.insert_one(item)
            # collection.update_one(item, {'$set': item}, upsert=True)
            # print()
            return item

        if spider.name == 'SuperJob':
            # print("___________")
            salary_list_sj = []
            for i in item['salary']:
                # new_salary = ''.join(salary)
                s = i.replace(" ", "").replace("\xa0", "")

                salary_list_sj.append(s)
                item['salary'] = salary_list_sj
                if item['salary'][0] == "Подоговорённости":
                    item['salary_min'] = None
                    item['salary_max'] = None
                elif 'от' in item:
                    item['salary_min'] = item['salary'][1]
                    item['salary_max'] = None

                elif 'до' in item:
                    item['salary_min'] = None
                    item['salary_max'] = item['salary'][2]

                elif len(item) > 3 and item['salary'][0] != 'от':
                    item['salary_min'] = int(item['salary'][0])
                    item['salary_max'] = int(item['salary'][1])

                else:
                    item['salary_min'] = item['salary'][0]
                    item['salary_max'] = item['salary'][0]

                collection = self.mongo_db[spider.name]
                # collection.update_one(item, {'$set': item}, upsert=True)
                collection.insert_one(item)
                # print()
            return item