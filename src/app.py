from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage
items = []

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(items), 200

@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
    
    item = {
        "id": len(items) + 1,
        "name": data['name']
    }
    items.append(item)
    return jsonify(item), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
