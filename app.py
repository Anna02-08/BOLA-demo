from flask import Flask, request, jsonify, render_template
from copy import deepcopy

app = Flask(__name__)

# Demo users and their tokens
TOKENS = {
    "alice-token": "alice",
    "bob-token": "bob"
}

# Simulated private documents
INITIAL_DOCUMENTS = {
    1: {
        "id": 1,
        "owner": "alice",
        "title": "Alice's private notes"
    },
    2: {
        "id": 2,
        "owner": "bob",
        "title": "Bob's secret project"
    }
}
documents = deepcopy(INITIAL_DOCUMENTS)

def get_current_user():
    auth = request.headers.get("Authorization", "")
    scheme, _, token = auth.partition(" ")

    if scheme.lower() != "bearer":
        return None

    return TOKENS.get(token)

######################################################
#########        API ENDPOINTS            ############
######################################################

@app.route("/")
def home():
    return render_template("index.html")

# VULNERABLE ENDPOINT
@app.route("/vulnerable/documents/<int:doc_id>",methods=["GET", "PUT", "DELETE"])
def vulnerable_document(doc_id):

    user = get_current_user()

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    document = documents.get(doc_id)

    if not document:
        return jsonify({"error": "Not found"}), 404

    # BOLA: No ownership verification!
    if request.method == "GET":
        return jsonify(document), 200

    if request.method == "PUT":
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON"}), 400

        if not isinstance(data.get("title"), str):
            return jsonify({"error": "Title must be a string"}), 400

        document["title"] = data["title"]

        return jsonify({
            "message": "Document updated",
            "document": document
        }), 200

    if request.method == "DELETE":
        del documents[doc_id]

        return jsonify({
            "message": "Document deleted"
        }), 200


# SECURE ENDPOINT
@app.route("/secure/documents/<int:doc_id>", methods=["GET", "PUT", "DELETE"])
def secure_document(doc_id):

    user = get_current_user()

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    document = documents.get(doc_id)

    if not document:
        return jsonify({"error": "Not found"}), 404

    # Object-level authorization
    if document["owner"] != user:
        return jsonify({"error": "Not found"}), 404
    if request.method == "GET":
        return jsonify(document), 200

    if request.method == "PUT":
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON"}), 400

        if not isinstance(data.get("title"), str):
            return jsonify({"error": "Title must be a string"}), 400

        document["title"] = data["title"]

        return jsonify({
            "message": "Document updated",
            "document": document
        }), 200

    if request.method == "DELETE":
        del documents[doc_id]

        return jsonify({
            "message": "Document deleted"
        }), 200

    return jsonify(document)


@app.route("/reset", methods=["POST"])
def reset_documents():

    documents.clear()
    documents.update(deepcopy(INITIAL_DOCUMENTS))

    return jsonify({
        "message": "Demo data restored",
        "documents": list(documents.values())
    }), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
