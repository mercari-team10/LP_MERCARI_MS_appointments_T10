import requests
import json
import os
from flask import Flask, request
from dotenv import load_dotenv
import sys
import psycopg2
import jwt
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import  rsa
from config import config



conn = None
try:
    # read connection parameters
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
    print('Error connecting to Database')
    sys.exit()

app = Flask(__name__)


key = None
load_dotenv()


def get_public_key() :
    global key
    r = requests.get(os.environ.get("PUBLIC_KEY_URL"))
    data = r.content
    key = load_pem_public_key(data)

get_public_key()

if key is None :
    print('Unable to retireve public key')
    sys.exit()


# DONE
@app.route("/doc_appnt",methods=['POST'])
def check_doc_status_ot() :
    args = request.get_json()
    hospital_id = args['hospital_id']
    start_time = args['start_time']
    end_time = args['end_time']
    symptoms = args['symptoms']
    doc_id = args['doc_id']
    encoded = requests.cookies.get('PatientAuth')
    decoded = jwt.decode(encoded, key, algorithms=["RS256"])
    patient_id = decoded['NHID']
    query = f'INSERT INTO doc_appnts( doc_id, patient_id,start_time,end_time,hospital_id,symptoms) VALUES ( %s, %s, to_timestamp(%s), to_timestamp(%s) , %s, %s ) '
    cur.execute(query,(doc_id,patient_id,start_time,end_time,hospital_id,symptoms))


#DONE
@app.route("/doc_appnt", methods = ['GET'])
def get_appnts_get() :
    args = request.get_json()
    hospital_id = args['hospital_id']
    doc_id = args['doc_id']
    encoded = requests.cookies.get('PatientAuth')
    decoded = jwt.decode(encoded, key, algorithms=["RS256"])
    patient_id = decoded['NHID']
    query = f'SELECT * from doc_appnts WHERE hospital_id = %s AND doc_id = %s AND patient_id = %s'
    cur.execute(query,(hospital_id,doc_id,patient_id))
    result = cur.fetchall()
    return result




#DONE
@app.route("/doc_appnt_single", methods = ['GET'])
def get_appnts_post() :
    args = request.get_json()
    patient_id = args['patient_id']
    encoded = requests.cookies.get('DoctorAuth')
    decoded = jwt.decode(encoded, key, algorithms=["RS256"])
    doc_id = decoded['doc_id']
    query = f'SELECT * from doc_appnts WHERE doc_id = %s AND patient_id = %s'
    cur.execute(query,(doc_id,patient_id))
    result = cur.fetchall()
    return result


# DONE
@app.route("/doc_appnt", methods = ['DELETE'])
def get_appnts() :
    args = request.get_json()
    apnt_id = args['appnt_id']
    encoded = requests.cookies.get('PatientAuth')
    decoded = jwt.decode(encoded, key, algorithms=["RS256"])
    patient_id = decoded['NHID']
    query = f'DELETE from doc_appnts WHERE appnt_id = %s'
    cur.execute(query,(apnt_id))
    result = cur.fetchall()
    return result


@app.route("/lab_appnt",methods=['POST'])
def check_doc_status() :
    args = request.get_json()
    lab_id = args['lab_id']
    report_time = args['report_time']
    test_id = args['test_id']
    encoded = requests.cookies.get('PatientAuth')
    decoded = jwt.decode(encoded, key, algorithms=["RS256"])
    patient_id = decoded['NHID']
    query = f'INSERT INTO lab_appnts( lab_id, patient_id,report_time,test_id) VALUES ( %s, %s, to_timestamp(%s), %s) '
    cur.execute(query,(lab_id,patient_id,report_time,test_id))


#DONE
@app.route("/lab_appnt", methods = ['GET'])
def get_appnts_t1() :
    args = request.get_json()
    lab_id = args['lab_id']
    test_id = args['test_id']
    encoded = requests.cookies.get('PatientAuth')
    decoded = jwt.decode(encoded, key, algorithms=["RS256"])
    patient_id = decoded['NHID']
    query = f'SELECT * from doc_appnts WHERE lab_id = %s AND test_id = %s AND patient_id = %s'
    cur.execute(query,(lab_id,test_id,patient_id))
    result = cur.fetchall()
    return result


# DONE
@app.route("/lab_appnt", methods = ['DELETE'])
def get_appnts_t2() :
    args = request.get_json()
    apnt_id = args['appnt_id']
    encoded = requests.cookies.get('PatientAuth')
    decoded = jwt.decode(encoded, key, algorithms=["RS256"])
    nhid = decoded['NHID']
    query = f'DELETE from lab_appnts WHERE appnt_id = %s'
    cur.execute(query,(apnt_id))
    result = cur.fetchall()
    return result


# ADD PROPER METHOD TO COMMUNICATE WITH CALENDAR API
@app.route('/check_availability',methods = ['GET'])
def check_availability() :
    args = request.get_json()
    encoded = requests.cookies.get('PatientAuth')
    decoded = jwt.decode(encoded, key, algorithms=["RS256"])
    nhid = decoded['NHID']
    start_time = args['start_time']
    duration = args['duration']
    hospital_id = args['hospital_id']
    doc_id = args['doc_id']
    params = {'nhid' : nhid,'start_time' : start_time,'duration' : duration,'hospital_id' : hospital_id, 'doc_id' : doc_id}
    r = requests.get(url = URL, params = params)
    data = r.json()
    return data['availability']

if __name__ == '__main__':
    app.run()