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


def pincode_group_delete_user(db, pincodes, user_id):
	user_id = ObjectId(user_id)
	
	for pincode in pincodes:
		group = db.search(collection=groups_collection, filters={"pincode" : pincode})
		if not group or group == 'null':
			continue
		current_user_ids = group.get('user_ids')
		if not current_user_ids or current_user_ids == 'null':
			current_user_ids = []

		if user_id in current_user_ids:
			current_user_ids = current_user_ids.remove(user_id)
			db.update(collection=groups_collection, filter={"pincode" : pincode}, record={ "$set": {"user_ids" : current_user_ids}})
	return db.search(collection=users_collection, filters={"_id" : user_id})

@app.route('/removePincode', methods=['GET', 'POST'])
def remove_pincode():
	data = request.json
	accepted_fields = [
		"telegram_id",
		"pincodes"
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

	data['pincodes'] = list(map(str, data['pincodes']))

	if db:
		# Check if user already exists
		existing_user = db.search(collection=users_collection, filters={"telegram_id" : data.get('telegram_id')})
		if existing_user and existing_user != 'null':
			# Update the pincodes
			current_pincodes = existing_user.get('pincodes')
			pincodes_to_delete = data.get('pincodes')
			if current_pincodes and current_pincodes != 'null':
				pincodes_to_update = list(set(current_pincodes) - (set(pincodes_to_delete)))
		
				db.update(collection=users_collection, filter={"telegram_id" : data.get('telegram_id')}, record={ "$set": {"pincodes" : pincodes_to_update} })

			user_data = pincode_group_delete_user(db, data.get('pincodes'), existing_user.get("_id"))

			return jsonify({"success" : True, "msg" : "You are an existing user, pincodes have been updated.", "user_data" : dumps(user_data)}), 200

		return jsonify({"success" : False, "msg" : f"User {data.get('telegram_id')} does not exist."}), 400

def pincode_group_add_or_update_user(db, pincodes, user_id):
	user_id = ObjectId(user_id)
	for pincode in pincodes:
		existing_record = db.search(collection=groups_collection, filters={"pincode" : pincode})
		if existing_record:
			# Check if user_id in list of user_ids
			existing_user_ids = existing_record.get('user_ids')
			if not existing_user_ids or existing_user_ids == 'null':
				existing_user_ids = []

			if user_id not in existing_user_ids:
				existing_user_ids.append(user_id)
				db.update(collection=groups_collection, filter={"pincode" : pincode}, record={ "$set": {"user_ids" : existing_user_ids}})
		else:
			db.insert(collection=groups_collection, record={
					"pincode" : pincode,
					"user_ids" : [user_id]
				})
	return db.search(collection=users_collection, filters={"_id" : user_id})

@app.route('/addPincode', methods=['GET', 'POST'])
def add_pincode():
	data = request.json
	accepted_fields = [
		"first_name",
		"last_name",
		"telegram_username",
		"telegram_id",
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

	data['pincodes'] = list(map(str, data['pincodes']))

	if db:
		# Check if user already exists
		existing_user = db.search(collection=users_collection, filters={"telegram_id" : data.get('telegram_id')})
		if existing_user and existing_user != 'null':
			# Update the pincodes
			current_pincodes = existing_user.get('pincodes')
			pincodes_to_update = data.get('pincodes')
			if current_pincodes and current_pincodes != 'null':
				pincodes_to_update = list(set(current_pincodes).union(set(pincodes_to_update)))

			db.update(collection=users_collection, filter={"telegram_id" : data.get('telegram_id')}, record={ "$set": {"pincodes" : pincodes_to_update} })

			user_data = pincode_group_add_or_update_user(db, data.get('pincodes'), existing_user.get("_id"))

			return jsonify({"success" : True, "msg" : "You are an existing user, pincodes have been updated.", "user_data" : dumps(user_data)}), 200

		record = db.insert(collection=users_collection, record=data)
		if record:
			user_data = pincode_group_add_or_update_user(db, data.get('pincodes'), record.get("_id"))
			return jsonify({"success" : True, "user_data" : dumps(user_data)}), 200

	return jsonify({"success" : False}), 500

@app.route('/findUser', methods=['POST'])
def user():
	data = request.json
	accepted_fields = [
		"telegram_id"
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

	user_data = db.search(collection=users_collection, filters={"telegram_id" : data.get('telegram_id')})
	return jsonify({"success" : True, "user" : dumps(user_data)}) 

if __name__ == '__main__':
	app.run(threaded=True, port=5000)






