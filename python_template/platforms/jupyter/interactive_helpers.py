import pandas as pd
import numpy as np
import json
import os
import boto3
import ast
from enum import Enum
import subprocess

class Platform(Enum):
    AWS = 1
    GCF = 2
    IBM = 3
    AZURE = 4

lastHash = ""
client = boto3.client('lambda')

defaultConfig = {
	"README": "See ./deploy/README.md for help!",

	"functionName": "hello",

	"lambdaHandler": "lambda_function.lambda_handler",
	"lambdaRoleARN": "",
	"lambdaSubnets": "",
	"lambdaSecurityGroups": "",
	"lambdaEnvironment": "Variables={EXAMPLEVAR1=VAL1,EXAMPLEVAR2=VAL2}",
	"lambdaRuntime": "python3.7",
	"googleHandler": "hello_world",
	"googleRuntime": "python37",
	"ibmRuntime": "python:3",
	"azureRuntime": "python",
    "test": {}
}

    
def interactive_preprocess(platforms, memory, config):
    data = None
    with open("interactive.ipynb") as f_in:
        data = json.load(f_in)
    
    sourceLines = data['cells'][3]['source']
    
    string = ""
    with open('handler.py', 'w') as handler:
        handler.write("# Generated by Interactive Notebook - ")
        for line in sourceLines:
            handler.write(line)
            string += line
    handler.close()
    
    test = hash(string)
    global lastHash
    if (lastHash == test):
        print("No changes detected. Make sure to save the notebook!")
        return None
    
    for key in config:
        defaultConfig[key] = config[key]
    with open('../deploy/interactiveConfig.json', 'w') as json_file:
        json.dump(defaultConfig, json_file)
    
    for platform in platforms:
        if (platform == platform.AWS):
            print("Starting ../deploy/publish.sh for AWS...")
            command = "../deploy/publish.sh 1 0 0 0 " + str(memory) + " interactiveConfig.json > ../deploy/aws-log.txt"
            print(subprocess.check_output(command.split()).decode('ascii'))
            print("Deploy Complete!\n")
        elif (platform == platform.GCF):
            print("Starting ../deploy/publish.sh for GCF..")
            command = "../deploy/publish.sh 0 1 0 0 " + str(memory) + " interactiveConfig.json > ../deploy/aws-log.txt"
            print(subprocess.check_output(command.split()).decode('ascii'))
            print("Deploy Complete!\n")
        elif (platform == platform.IBM):
            print("Starting ../deploy/publish.sh for IBM..")
            command = "../deploy/publish.sh 0 0 1 0 " + str(memory) + " interactiveConfig.json > ../deploy/aws-log.txt"
            print(subprocess.check_output(command.split()).decode('ascii'))
            print("Deploy Complete!\n")
        elif (platform == platform.AZURE):
            print("Starting ../deploy/publish.sh for Azure..")
            command = "../deploy/publish.sh 0 0 0 1 " + str(memory) + " interactiveConfig.json > ../deploy/aws-log.txt"
            print(subprocess.check_output(command.split()).decode('ascii'))
            print("Deploy Complete!\n")
            
    lastHash = test
    
def run_on_cloud(payload):
    response = client.invoke(
        FunctionName = 'hello',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    if 'Payload' in response:
        stream = response['Payload']
        data = ast.literal_eval(stream.read().decode("UTF-8"))
        
        frame = {
            'Attribute': list(data.keys()),
            'Value': list(data.values())
        }
        return pd.DataFrame.from_dict(frame)
    else:
        print(str(response))
        
def test_on_cloud(platforms, payload, config):
    
    for key in config:
        defaultConfig[key] = config[key]
        
    defaultConfig['test'] = payload
        
    with open('../deploy/interactiveConfig.json', 'w') as json_file:
        json.dump(defaultConfig, json_file)
        
    for platform in platforms:
        if (platform == platform.AWS):
            command = "../deploy/test.sh 1 0 0 0 512 interactiveConfig.json"
            print(subprocess.check_output(command.split()).decode('ascii'))
        elif (platform == platform.GCF):
            command = "../deploy/test.sh 0 1 0 0 512 interactiveConfig.json"
            print(subprocess.check_output(command.split()).decode('ascii'))
        elif (platform == platform.IBM):
            command = "../deploy/test.sh 0 0 1 0 512 interactiveConfig.json"
            print(subprocess.check_output(command.split()).decode('ascii'))
        elif (platform == platform.AZURE):
            command = "../deploy/test.sh 0 0 0 1 512 interactiveConfig.json"
            print(subprocess.check_output(command.split()).decode('ascii'))