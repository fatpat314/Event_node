import config
from dotenv import load_dotenv
from flask import Flask, jsonify, request, session, g
from flask_jwt_extended import JWTManager, jwt_required, \
                               create_access_token, get_jwt_identity
import requests, names, random, threading, uuid, json
import argparse
import ast

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY # change this to a random string in production
CNM_url = "http://localhost:6000"
KAN_url = "http://localhost:8050"
jwt = JWTManager(app)
load_dotenv()

@app.route('/', methods = ['GET'])
def home():
    if(request.method == 'GET'):
        data = "Event Node!"
        return jsonify({'data': data})

@app.route('/event-patient-provider', methods = ['GET', 'POST'])
def event_patient_provider():
    try:
        patient_id = [request.json.get('patient_id')]
        provider_id = [request.json.get('provider_id')]
        send_vertex = 'Care_Provider'
        receive_vertex = 'Patient'
        # add edge info
        send_edge_name = 'event_care_provider'
        receive_edge_name = 'event_patient'
        print("ID:", patient_id, provider_id)
        # Send to CNM to create event
        CNM_url_symptoms = f'{CNM_url}/add_event'
        data = {'vertex1_id_list': provider_id, 'vertex2_id_list': patient_id, 'send_vertex': send_vertex, 'receive_vertex': receive_vertex, 'send_edge_name': send_edge_name, 'receive_edge_name': receive_edge_name}
        requests.post(CNM_url_symptoms, json=data)
    except:
        pass
    return('hi')

@app.route('/event-patient-symptoms', methods = ['GET', 'POST'])
def event_patient_symptoms():
    patient_id = [request.json.get('patient_id')]
    symptoms_id = request.json.get('symptoms_id')
    send_vertex = 'Patient'
    receive_vertex = 'Symptom'
    send_edge_name = 'event_patient'
    receive_edge_name = 'event_symptom'

    CNM_url_symptoms = f'{CNM_url}/add_event'
    data = {'vertex1_id_list': patient_id, 'vertex2_id_list': symptoms_id, 'send_vertex': send_vertex, 'receive_vertex': receive_vertex, 'send_edge_name': send_edge_name, 'receive_edge_name': receive_edge_name}
    requests.post(CNM_url_symptoms, json=data)

    return('hi')

@app.route('/event-symptoms-diseases', methods = ['GET', 'POST'])
def event_symptoms_diseases():
    symptoms_id = request.json.get('symptoms_id')
    diseases_id = request.json.get('diseases_id')
    symptoms_id = ast.literal_eval(symptoms_id)
    diseases_id = ast.literal_eval(diseases_id)
    send_vertex = 'Symptom'
    receive_vertex = 'Disease'
    send_edge_name = 'event_symptom'
    receive_edge_name = 'event_disease'

    CNM_url_symptoms_diseases = f'{CNM_url}/add_event'
    data = {'vertex1_id_list': symptoms_id, 'vertex2_id_list': diseases_id, 'send_vertex': send_vertex, 'receive_vertex': receive_vertex, 'send_edge_name': send_edge_name, 'receive_edge_name': receive_edge_name}
    requests.post(CNM_url_symptoms_diseases, json=data)

    return('hi')

@app.route('/event-diagnosis', methods = ['GET', 'POST'])
def event_diagnosis():
    provider_id = [request.json.get('provider_id')]
    patient_id = [request.json.get('patient_id')]
    disease_id = [request.json.get('disease_id')]

    send_vertex = 'Disease'
    receive_vertex = 'Patient'
    send_edge_name = 'event_disease'
    receive_edge_name = 'event_patient'

    CNM_url_diagnosis = f'{CNM_url}/add_event'
    data = {'vertex1_id_list': disease_id, 'vertex2_id_list': patient_id, 'send_vertex': send_vertex, 'receive_vertex': receive_vertex, 'send_edge_name': send_edge_name, 'receive_edge_name': receive_edge_name}
    requests.post(CNM_url_diagnosis, json=data)

    send_vertex = 'Disease'
    receive_vertex = 'Care_Provider'
    send_edge_name = 'event_disease'
    receive_edge_name = 'event_care_provider'

    data = {'vertex1_id_list': disease_id, 'vertex2_id_list': provider_id, 'send_vertex': send_vertex, 'receive_vertex': receive_vertex, 'send_edge_name': send_edge_name, 'receive_edge_name': receive_edge_name}
    requests.post(CNM_url_diagnosis, json=data)

    # Disease to patient
    # Disease to provider
    return('hi')

@app.route('/event-risk', methods = ['GET', 'POST'])
def event_risk():
    patient_id = [request.json.get('patient_id')]
    risk_factors_id = request.json.get('risk_factors_id')
    print("EVENT RISK:", patient_id, risk_factors_id)

    send_vertex = 'Patient'
    receive_vertex = 'Risk_Factors'
    send_edge_name = 'event_patient'
    receive_edge_name = 'event_risk'

    CNM_url_event = f'{CNM_url}/add_event'
    data = {'vertex1_id_list': patient_id, 'vertex2_id_list': risk_factors_id, 'send_vertex': send_vertex, 'receive_vertex': receive_vertex, 'send_edge_name': send_edge_name, 'receive_edge_name': receive_edge_name}
    requests.post(CNM_url_event, json=data)

    return('hi')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8020, help="Port to run the server on")
    args = parser.parse_args()
    port = args.port
    app.run(host="0.0.0.0", port=port)