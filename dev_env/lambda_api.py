import json
import boto3
import requests
import time

def lambda_handler(event, context):
    # Jenkins details
    jenkins_base_url = "http://13.49.230.243:8080"
    job_name = "developer%20enviroment"  # URL-encoded job name
    jenkins_token = "abc-123"
    jenkins_user = "<jenkins_username>"
    jenkins_password = "<jenkins_password>"
    
    param1 = event['queryStringParameters'].get("param1", "")
    param2 = event['queryStringParameters'].get("param2", "")
    trigger_url = f"{jenkins_base_url}/job/{job_name}/buildWithParameters?token={jenkins_token}&param1={param1}&param2={param2}"

    response = requests.get(trigger_url, auth=(jenkins_user, jenkins_password))

    if response.status_code != 201:
        return {
            'statusCode': response.status_code,
            'body': json.dumps(f"Failed to trigger Jenkins job: {response.text}")
        }
    
    eks_client = boto3.client("eks", region_name="eu-north-1")
    elb_client = boto3.client("elbv2", region_name="eu-north-1")
    cluster_name = "production-test-cluster"
    
    try:
        eks_client.describe_cluster(name=cluster_name)

        load_balancers = elb_client.describe_load_balancers().get('LoadBalancers', [])
        
        if not load_balancers:
            return {
                'statusCode': 404,
                'body': json.dumps("No load balancers found")
            }
        
        latest_lb = max(load_balancers, key=lambda lb: lb['CreatedTime'])
        load_balancer_url = latest_lb['DNSName']
        print(load_balancer_url)
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error retrieving load balancer URL: {str(e)}")
        }

    return {
        'statusCode': 200,
        'body': json.dumps({"loadBalancerUrl": load_balancer_url})
    }
