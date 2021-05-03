import os
from db import DB
from flask import Flask, request, jsonify
from bson.objectid import ObjectId
from bson.json_util import dumps

'''
	Registration API 
'''

app = Flask(__name__)
db = DB(os.getenv("MONGO_CONN_URL")).connect(os.getenv("DATABASE"))

users_collection = os.getenv("USER_COLLECTION")
groups_collection = os.getenv("GROUPS_COLLECTION")


def pincode_group_add_or_update_user(db, pincodes, user_id):
	for pincode in pincodes:
		existing_record = db.search(collection=groups_collection, filters={"pincode" : pincode})
		if existing_record:
			# Check if user_id in list of user_ids
			existing_user_ids = existing_record.get('user_ids')
			if user_id not in existing_user_ids:
				existing_user_ids.append(user_id)
				db.update(collection=groups_collection, filter={"pincode" : pincode}, record={ "$set": {"user_ids" : existing_user_ids}})
		else:
			db.insert(collection=groups_collection, record={
					"pincode" : pincode,
					"user_ids" : [user_id]
				})

@app.route('/register', methods=['GET', 'POST'])
def register():
	data = request.get_json(force=True)
	accepted_fields = [
		"telegram_username",
		"pincodes",
		"chat_id"
	]

	unexpected_fields = []

	for input_field in data:
		# Found mandaotry field
		if input_field in accepted_fields:
			accepted_fields.remove(input_field)
		else:
			unexpected_fields.append(input_field)

	if unexpected_fields or accepted_fields:
		return jsonify({"success" : False, "unexpected_fields" : unexpected_fields, "missing_fields" : accepted_fields}), 400

	if db:
		# Check if user already exists
		existing_user = db.search(collection=users_collection, filters={"telegram_username" : data.get('telegram_username')})
		if existing_user and existing_user != 'null':
			# Update the pincodes
			db.update(collection=users_collection, filter={"telegram_username" : data.get('telegram_username')}, record={ "$set": {"pincodes" : data.get('pincodes')} })

			pincode_group_add_or_update_user(db, data.get('pincodes'), existing_user.get("_id"))

			return jsonify({"success" : True, "msg" : "You are an existing user, pincodes have been updated."}), 200

		record = db.insert(collection=users_collection, record=data)
		if record:
			pincode_group_add_or_update_user(db, data.get('pincodes'), record.get("_id"))
			return jsonify({"success" : True, "inserts" : [dumps(record)]}), 200

	return jsonify({"success" : False}), 500



if __name__ == '__main__':
	app.run(port=5000)






