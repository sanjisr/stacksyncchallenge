from flask import Flask, request, jsonify
from execute import run_script
import json

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json()
    #input validation
    if not data or 'script' not in data:
        return jsonify({'error': 'Missing "script" key in request body'}), 400

    script = data['script']
    try:
        # result, stdout = run_script(script)
        # return jsonify({'result': result, 'stdout': stdout})
        result, stdout = run_script(script)
        return {"result": result, "stdout": stdout}
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
