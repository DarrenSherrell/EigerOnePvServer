from flask import Flask, request, jsonify
import epics

# test

app = Flask(__name__)

# Endpoint to get the value of a PV
@app.route('/pv/<string:pvname>', methods=['GET'])
def get_pv(pvname):
    value = epics.caget(pvname, as_string=True)
    if value is not None:
        return jsonify({'pvname': pvname, 'value': value}), 200
    else:
        return jsonify({'error': f'PV {pvname} not found'}), 404

# Endpoint to set the value of a PV
@app.route('/pv/<string:pvname>', methods=['POST'])
def set_pv(pvname):
    data = request.get_json()
    if not data or 'value' not in data:
        return jsonify({'error': 'No value provided'}), 400

    value_to_set = data['value']

    pv = epics.PV(pvname)
    pv.wait_for_connection(timeout=2.0)
    if not pv.connected:
        return jsonify({'error': f'PV {pvname} not found'}), 404

    if pv.enum_strs:
        # If the value is a string, find its corresponding index
        if isinstance(value_to_set, str):
            try:
                index = pv.enum_strs.index(value_to_set)
                value_to_set = index
            except ValueError:
                return jsonify({'error': f'Invalid enum value for {pvname}'}), 400
    else:
        # Convert value to the appropriate type
        try:
            value_to_set = type(pv.value)(value_to_set)
        except ValueError:
            return jsonify({'error': 'Invalid value type'}), 400

    success = pv.put(value_to_set)
    if success:
        return jsonify({'pvname': pvname, 'value_set_to': data['value']}), 200
    else:
        return jsonify({'error': f'Failed to set PV {pvname}'}), 500

# Example endpoint to start acquisition
@app.route('/acquire/start', methods=['POST'])
def start_acquisition():
    pvname = '21EIG1:cam1:Acquire'
    epics.caput(pvname, 1)
    return jsonify({'status': 'Acquisition started'}), 200

# Example endpoint to stop acquisition
@app.route('/acquire/stop', methods=['POST'])
def stop_acquisition():
    pvname = '21EIG1:cam1:Acquire'
    epics.caput(pvname, 0)
    return jsonify({'status': 'Acquisition stopped'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
