import os
from pymongo import MongoClient
import json
import config as conf

# -----------------------------------economy--------------------------------------------

class Database:
    def __init__(self):
        config = conf.Config()
        self.cluster = MongoClient(config.DATABASE_URL)
        self.info = self.cluster['info']
        self.economy = self.cluster['Economy']

    def inventory(self, user_id):
        user = self.economy['Inventory'].find_one({'_id': user_id})
        if user is None:
            user = {'_id': user_id, 'items': {}}
            self.economy['Inventory'].insert_one(user)
        else:
            pass
        return user

    def check_account(self, user_id):
        currency = self.economy['Currency']
        user = currency.find_one({'_id': user_id})
        if user is None:
            user = {'_id': user_id, 'wallet': 0, 'bank': 0}
            currency.insert_one(user)
        else:
            pass
        return user


    def add_in_wallet(self, user_id, amount):
        user = self.check_account(user_id)
        money = int(user['wallet'])
        self.economy['Currency'].update_one(
            {'_id': user_id}, {'$set': {'wallet': money+int(amount)}})


    def add_in_bank(self, user_id, amount):
        user = self.check_account(user_id)
        money = int(user['bank'])
        self.economy['Currency'].update_one(
            {'_id': user_id}, {'$set': {'bank': money+int(amount)}})


    def get_item_from_inventory (self, user_id):
        user = self.economy['Inventory'].find_one({'_id': user_id})
        if user is None:
            user = {'_id': user_id, 'items': {}}
            self.economy['Inventory'].insert_one(user)
        else:
            pass
        return user


    def add_item(self, user_id, item, amount):
        inventory = self.get_item_from_inventory(user_id)
        items = inventory['items']
        try:
            amounts = items[item]
        except:
            amounts = 0
        amounts += int(amount)
        items[item] = int(amounts)
        self.economy['Inventory'].update_one(
            {'_id': user_id}, {'$set': {'items': items}})


    def remove_from_wallet(self, user_id, amount):
        user = self.check_account(user_id)
        money = int(user['wallet'])
        self.economy['Currency'].update_one(
            {'_id': user_id}, {'$set': {'wallet': money-int(amount)}})


    def remove_from_bank(self, user_id, amount):
        user = self.check_account(user_id)
        money = int(user['bank'])
        self.economy['Currency'].update_one(
            {'_id': user_id}, {'$set': {'bank': money-int(amount)}})


    def remove_item(self, user_id, item, amount):
        inventory = self.get_item_from_inventory (user_id)
        items = inventory['items']
        try:
            amount = items[item]
        except:
            amount = 0
        amount -= int(amount)
        items[item] = int(amount)
        self.economy['Inventory'].update_one(
            {'_id': user_id}, {'$set': {'items': items}})

    # ---------------------------------------------------------------------Leveling-------------------------------------------------------------------------------


    def get_leveling_info(self, user_id):
        user = self.info['leveling'].find_one({'_id': user_id})
        if user is None:
            user = {'_id': user_id, 'experience': 0, 'level': 1}
            self.info['leveling'].insert_one(user)
        else:
            pass
        return user


    def add_experience(self, user_id, amount):
        user = self.get_leveling_info(user_id)
        experience = user['experience']
        experience += int(amount)
        self.info['leveling'].update_one({'_id': user_id}, {'$set': {'experience': experience}})


    def level_up(self, user_id):
        user = self.get_leveling_info(user_id)
        experience = user['experience']
        level = user['level']
        # print(user)
        experience_required = 10 * 1.5 **level
        # print(experience_required)
        if experience >= experience_required:
            self.info['leveling'].update_one(
                {'_id': user_id}, {'$set': {'level': level+1}})
            return True
        return False

# def check_key(key):
#     isKey = self.info['keys'].find_one({'Key': key})
#     if isKey is None:
#         return False
#     else:
#         return True