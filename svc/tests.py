import os
from .db import DB
from bson.objectid import ObjectId

'''
	Registration API Test - TBA
'''
###########################################
#                   TBA                   #
###########################################

'''
	DB Tests
'''

CONN_STRING = os.getenv("MONGO_CONN_URL")
DB_NAME = os.getenv("DATABASE")

# Group Collection Tests
GROUPS_COLLECTION = os.getenv("GROUPS_COLLECTION")

###########################################
#                   TBA                   #
###########################################

# User Collection Tests
USER_COLLECTION = os.getenv("USER_COLLECTION")

def test_user_insert():
	db = DB(CONN_STRING).connect(DB_NAME)
	test_user = {
		"telegram_username" : "iamblizzy"
	}
	# Test `insert`
	test_user_id = db.insert(collection=USER_COLLECTION, record=test_user).get("_id")
	result = db.instance[USER_COLLECTION].find_one({"_id" : test_user_id})

	# Clean up
	db.instance[USER_COLLECTION].delete_one({"_id" : test_user_id})

	assert result == test_user


def test_user_delete():
	db = DB(CONN_STRING).connect(DB_NAME)
	test_user = {
		"telegram_username" : "iamblizzy"
	}
	# Test `delete`
	test_user_id = db.instance[DB_NAME].insert_one(test_user).inserted_id
	db.delete(collection=USER_COLLECTION, record=test_user)
	result = db.instance[USER_COLLECTION].find_one({"_id" : test_user_id})

	# Clean up
	db.instance[USER_COLLECTION].delete_one({"_id" : test_user_id})

	assert result == None

def test_user_update():
	db = DB(CONN_STRING).connect(DB_NAME)
	test_user = {
		"telegram_username" : "iamblizzy"
	}
	# Test `update`
	test_user_id = db.instance[USER_COLLECTION].insert_one(test_user).inserted_id
	update_test_user_fields = { "$set": {"telegram_username" : "iamlazy"} }
	db.update(collection=USER_COLLECTION, filter={"_id" : test_user_id}, record=update_test_user_fields)
	expected = {
		"_id" : test_user_id,
		"telegram_username" : "iamlazy"
	}
	result = db.instance[USER_COLLECTION].find_one({"_id" : test_user_id})

	# Clean up
	db.instance[USER_COLLECTION].delete_one({"_id" : test_user_id})

	assert result == expected

def test_user_search():
	db = DB(CONN_STRING).connect(DB_NAME)
	test_user = {
		"telegram_username" : "iamblizzy"
	}
	# Test `read`
	test_user_id = db.instance[USER_COLLECTION].insert_one(test_user).inserted_id
	result = db.search(collection=USER_COLLECTION, filters={"_id" : test_user_id}, all=False)

	# Clean up
	db.instance[USER_COLLECTION].delete_one({"_id" : test_user_id})

	assert result == test_user