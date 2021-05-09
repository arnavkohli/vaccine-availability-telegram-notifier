import pymongo, json

def handle_db_exception(func):
	def wrapper(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except Exception as err:
			print (f"[DB] There was error [{func.__name__}]: {err}")
		return False
	return wrapper

class DB:
	def __init__(self, conn_string):
		self.conn_string = conn_string

	@handle_db_exception
	def connect(self, db_name):
		self.client = pymongo.MongoClient(self.conn_string)
		self.instance = self.client[db_name]
		return self

	@handle_db_exception
	def insert(self, collection, record):
		self.instance[collection].insert_one(record)
		return record

	@handle_db_exception
	def delete(self, collection, record):
		self.instance[collection].delete_one(record)
		return None

	@handle_db_exception
	def update(self, collection, filter, record):
		self.instance[collection].update_one(filter, record)
		return record

	@handle_db_exception
	def search(self, collection, filters=None, all=False):
		if all:
			return [doc for doc in self.instance[collection].find(filters)]
		return self.instance[collection].find_one(filters)
