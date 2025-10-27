# import uuid
# from flask import Blueprint, request, jsonify
# from firebase_admin import firestore
# from flask_cors import cross_origin

# db = firestore.client()
# user_Ref = db.collection('user')

# userAPI = Blueprint('userAPI', __name__)

# # for post methods
# @userAPI.route('/add', methods=['POST'])
# def create():
#     try:
#         id = uuid.uuid4()
#         user_Ref.document(id.hex).set(request.json)
#         return jsonify({"success":True}), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"

# # for get methods
# @userAPI.route('/list')
# def read():
#     try:
#         all_users = [doc.to_dict() for doc in user_Ref.stream()]
#         return jsonify(all_users), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"
    
# @userAPI.route('/sendImage', methods=['POST'])
# def parse_create():
#     try:
#         print("Received image data:", request.json)  # Print received data for debugging
#         return jsonify({"success": True}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500