from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Demo users and their tokens
TOKENS = {
    "alice-token": "alice",
    "bob-token": "bob"
}

# Simulated private documents
documents = {
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
@app.route("/vulnerable/documents/<int:doc_id>")
def vulnerable_document(doc_id):

    user = get_current_user()

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    document = documents.get(doc_id)

    if not document:
        return jsonify({"error": "Not found"}), 404

    # BOLA: No ownership verification!
    return jsonify(document)


# SECURE ENDPOINT
@app.route("/secure/documents/<int:doc_id>")
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

    return jsonify(document)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
