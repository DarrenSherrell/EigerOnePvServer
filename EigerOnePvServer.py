from flask import Flask, request, jsonify
import epics
import numpy as np

app = Flask(__name__)


# GET the value of a PV
@app.route('/pv/<string:pvname>', methods=['GET'])
def get_pv(pvname):
    print(f"PV Name: {pvname}")
    pv = epics.PV(pvname)
    pv.wait_for_connection(timeout=2.0)
    if not pv.connected:
        return jsonify({'error': f'PV {pvname} not found'}), 404
    pv_type = pv.type.lower()        # e.g., 'time_char', 'ctrl_float', etc.
    pv_base_type = pv_type.split('_')[-1]  # Extract base type
    pv_count = pv.count
    print(f"PV Type: {pv_type}")
    print(f"PV Base Type: {pv_base_type}")
    print(f"PV Count: {pv_count}")
    value = epics.caget(pvname, as_string=True)
    if value is not None:
        print(f"PV Value: {value}")
        return jsonify({'pvname': pvname, 'value': value}), 200
    else:
        return jsonify({'error': f'PV {pvname} not found'}), 404


# POST a value to a PV
@app.route('/pv/<path:pvname>', methods=['POST'])
def set_pv(pvname):
    data = request.get_json()
    if not data or 'value' not in data:
        return jsonify({'error': 'No value provided'}), 400

    value_to_set = data['value']

    pv = epics.PV(pvname)
    pv.wait_for_connection(timeout=2.0)
    if not pv.connected:
        return jsonify({'error': f'PV {pvname} not found'}), 404

    pv_type = pv.type.lower()        # e.g., 'time_char', 'ctrl_float', etc.
    pv_base_type = pv_type.split('_')[-1]  # Extract base type
    pv_count = pv.count

    print(f"PV Name: {pvname}")
    print(f"PV Type: {pv_type}")
    print(f"PV Base Type: {pv_base_type}")
    print(f"PV Count: {pv_count}")

    if pv_base_type == 'enum':
        # Handle enum PVs
        if isinstance(value_to_set, str):
            try:
                index = pv.enum_strs.index(value_to_set)
                value_to_set = index
            except ValueError:
                return jsonify({'error': f'Invalid enum value for {pvname}'}), 400
        else:
            try:
                value_to_set = int(value_to_set)
            except ValueError:
                return jsonify({'error': f'Invalid enum value for {pvname}'}), 400
    elif (pv_base_type == 'char' and pv_count > 1) or pv_base_type == 'string':
        # Handle string PVs (char waveform or string PVs)
        value_to_set = str(value_to_set)
    else:
        # For scalar numeric PVs
        try:
            value_to_set = float(value_to_set)
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid value type'}), 400

    # Try to set the PV value
    try:
        success = pv.put(value_to_set, wait=True)
        if success is not None:
            print(f"PV Value: {data['value']}")
            return jsonify({'pvname': pvname, 'value_set_to': data['value']}), 200
        else:
            return jsonify({'error': f'Failed to set PV {pvname}'}), 500
    except Exception as e:
        return jsonify({'error': f'Failed to set PV {pvname}: {str(e)}'}), 500


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
