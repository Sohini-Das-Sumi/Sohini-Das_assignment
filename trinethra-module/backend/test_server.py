from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    print("✅ Health check hit!")
    return jsonify({"status": "OK"})

@app.route('/api/analyze_single', methods=['POST'])
def analyze():
    print("✅ API endpoint hit!")
    data = request.get_json(silent=True)
    print(f"Data received: {data}")
    return jsonify({
        "status": "success",
        "received": data.get('transcript', 'no transcript'),
        "score": 8.5
    })

if __name__ == '__main__':
    print("🚀 Test server starting...")
    app.run(host='0.0.0.0', port=5177, debug=True)