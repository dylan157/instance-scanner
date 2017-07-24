import boto3
from boto3.dynamodb.conditions import Key, Attr
from collections import defaultdict
import awscli

ec2 = boto3.resource('ec2')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('interview_test')

def display(id):
    
    try: # find instance in database
        response = table.get_item(Key={'instance_id': id,})
        item = response['Item']
        #print json (I think)
        for key, value in item.items() :
            print (key+': ', value)
    except:
        print("instance not found")

def scan():
    # Get information for all instances
    running_instances = ec2.instances.filter(Filters=[{ 'Name': 'instance-state-name', 'Values': ['*']}])

    ec2info = defaultdict()

    for instance in running_instances:
        for tag in instance.tags:
            if 'Name'in tag['Key']:
                name = tag['Value']

        # Add instance info to a dictionary         
        ec2info[instance.id] = {'Instance Id': instance.instance_id,'Type': instance.instance_type,'State': instance.state['Name'],'Image Id': instance.image_id}

    attributes = ['Instance Id', 'State', 'Type', 'Image Id']
    titles = ['instance_id', 'State_Name', 'InstanceType', 'ImageId']

    #print and store in database
    for instance_id, instance in ec2info.items():
        stuff = []
        for key in attributes:
            print("{0}: {1}".format(key, instance[key]))
            stuff.append(instance[key])
        print("------")

        try: #check if instance id in database. If true, update each value.
            table.get_item(Key={'instance_id': stuff[0]})
            counter = 1
            #iterate through each 'column' in 'row' and replace value.
            for item in stuff:
                table.update_item(Key={'instance_id': stuff[0]},UpdateExpression='SET '+titles[counter]+' = :val1', ExpressionAttributeValues={':val1': item})
                counter += 1
        except:#Else, insert new data.
                table.put_item(Item={'instance_id': stuff[0],'State_Name': stuff[1],'InstanceType': stuff[2],'ImageId': stuff[3]})

def remove(id):
    try: 
        table.delete_item(Key={'instance_id': id})
        print("Instance record deleted")
    except: print("Instance not found/deleted")

def all():
    response = table.scan(('instance_id'))
    results = response['Items']
    for item in results:
        for key, value in item.items():
            print (key+': ', value)
        print("-------")

