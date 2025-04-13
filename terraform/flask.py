from flask import Flask, request, jsonify
import boto3
import requests
import logging
import os
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

aws_access_key_id = os.environ.get('ACCESS_KEY')
aws_secret_access_key = os.environ.get('SECRET_KEY')

@app.route('/get_public_ip', methods=['GET', 'POST'])
def get_public_ip():
    body = request.get_json()
    base_url = body["base_url"]
    driver_id = body['driver_id']

    region = body["region"]

    ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)
    try:
        url = f"http://{base_url}:6066/v1/submissions/status/{driver_id}"
        response = requests.get(url)
        result = response.json()
        logger.info(f'Got response from {url}: {result}')
        result = dict(result)
        private_ip = result["workerHostPort"].split(":")[0]
        public_ip = get_public_ip_from_private_ip(private_ip, ec2)
        try:
            url = f"http://{public_ip}:4040/api/v1/applications"
            response = requests.get(url)
            applications = response.json()
            app = dict(applications[0])
            app_id = app["id"]
            url = f"http://{public_ip}:4040/api/v1/applications/{app_id}/jobs"
            response = requests.get(url)
            jobs = response.json()
            job = dict(jobs[0])

        except Exception as e:
            url = f"http://{public_ip}:18080/api/v1/applications"
            response = requests.get(url)
            applications = response.json()
            app = dict(applications[0])
            app_id = app["id"]
            url = f"http://{public_ip}:18080/api/v1/applications/{app_id}/jobs"
            response = requests.get(url)
            jobs = response.json()

        result["app_id"] = app_id
        result["job_details"] = jobs


        result["public_ip"] = public_ip
        return jsonify(result)
    except Exception as e:
        logger.error(f'Error: {e}')
        return jsonify({"error": str(e)})

@app.route('/get_status', methods=['GET', 'POST'])
def get_status():
    body = request.get_json()
    base_url = body["base_url"]
    driver_id = body['driver_id']
    region = body["region"]

    ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)
    try:
        url = f"http://{base_url}:6066/v1/submissions/status/{driver_id}"
        response = requests.get(url)
        result = response.json()
        logger.info(f'Got response from {url}: {result}')
        result = dict(result)
        private_ip = result["workerHostPort"].split(":")[0]
        public_ip = get_public_ip_from_private_ip(private_ip, ec2)
        try:
            url = f"http://{public_ip}:4040/api/v1/applications"
            response = requests.get(url)
            applications = response.json()
            app = dict(applications[0])
            app_id = app["id"]
            url = f"http://{public_ip}:4040/api/v1/applications/{app_id}/jobs"
            response = requests.get(url)
            jobs = response.json()
            job = dict(jobs[0])

        except Exception as e:
            url = f"http://{public_ip}:18080/api/v1/applications"
            response = requests.get(url)
            applications = response.json()
            app = dict(applications[0])
            app_id = app["id"]
            url = f"http://{public_ip}:18080/api/v1/applications/{app_id}/jobs"
            response = requests.get(url)
            jobs = response.json()

        result["app_id"] = app_id
        result["job_details"] = jobs


        result["public_ip"] = public_ip
        return jsonify(result)
    except Exception as e:
        logger.error(f'Error: {e}')
        return jsonify({"error": str(e)})
    
@app.route('/get_submission_status', methods=['GET', 'POST'])
def get_submission_status():
    body = request.get_json()
    base_url = body["base_url"]
    driver_id = body['driver_id']

    region = body["region"]

    ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)
    try:
        url = f"http://{base_url}:6066/v1/submissions/status/{driver_id}"
        response = requests.get(url)
        result = response.json()
        logger.info(f'Got response from {url}: {result}')
        result = dict(result)
        private_ip = result["workerHostPort"].split(":")[0]
        public_ip = get_public_ip_from_private_ip(private_ip, ec2)

        result["public_ip"] = public_ip
        if result["driverState"] == "FAILED":
            result["driverState"] = "FAILED"
        if result["driverState"] == "FINISHED":
            result["driverState"] = "COMPLETED"
        if result["driverState"] == "RUNNING":
            result["driverState"] = "RUNNING"
        return jsonify(result)
    except Exception as e:
        logger.error(f'Error: {e}')
        return jsonify({"error": str(e)})
    
    
def get_public_ip_from_private_ip(private_ip, ec2):
    try:
        response = ec2.describe_instances(Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ])

        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                if instance.get('PrivateIpAddress') == private_ip:
                    return instance.get('PublicIpAddress')
    except Exception as e:
        logger.error(f'Error while getting public IP from private IP: {e}')

    return None

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)