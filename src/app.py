"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

jackson_family.add_member({
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
})
jackson_family.add_member({
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
})
jackson_family.add_member({
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
})

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/members', methods =['GET'])
def get_all_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/member/<int:member_id>', methods=['GET'])
def get_single_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if not member:
            return jsonify ({"error": "Member not found"}), 404
        return jsonify(member), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/member', methods=['POST'])
def add_member():
    try:
        body = request.get_json()
        if not body or "first_name" not in body or "age" not in body or "lucky_numbers" not in body:
            return jsonify({"error": "Missing required fields"}), 400

        jackson_family.add_member(body)
        return jsonify(jackson_family.get_all_members()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if not member:
            return jsonify({"error": "member not found bitch*s"}), 404

        jackson_family.delete_member(member_id)
        return jsonify({"done": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }


    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
