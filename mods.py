import boto3
from boto3.dynamodb.conditions import Key, Attr
from collections import defaultdict
import awscli

ec2 = boto3.resource('ec2')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('interview_test')

def display(id):
    
    try: # find instance in database
        db_attribute_ = table.get_item(Key={'instance_id': id,})
        item = db_instance_info['Item']
        #print json (I think)
        for key, value in item.items() :
            print (key+': ', value)
    except:
        print("instance not found")

def scan():
    # Get information for all instances
    running_instances = ec2.instances.filter()

    ec2info = defaultdict()

    for instance in running_instances:
        for tag in instance.tags:
            if 'Name'in tag['Key']:
                name = tag['Value']

        # Add instance info to a dictionary         
        ec2info[instance.id] = {'Instance Id': instance.instance_id,'Type': instance.instance_type,'State': instance.state['Name'],'Image Id': instance.image_id}

    ec2_instance_keys = ['Instance Id', 'State', 'Type', 'Image Id']
    db_attribute_id = ['instance_id', 'State_Name', 'InstanceType', 'ImageId']

    #print and store in database
    for instance_id, instance in ec2info.items():
        ec2_instance_info = []
        for key in ec2_instance_keys:
            print("{0}: {1}".format(key, instance[key]))
            ec2_instance_info.append(instance[key])
        print("------")

        try: #check if instance id in database. If true, update each value.
            table.get_item(Key={'instance_id': ec2_instance_info[0]})
            counter = 1
            #iterate through each 'column' in 'row' and replace value.
            for item in ec2_instance_info:
                table.update_item(Key={'instance_id': ec2_instance_info[0]},UpdateExpression='SET '+db_attribute_id[counter]+' = :val1', ExpressionAttributeValues={':val1': item})
                counter += 1
        except:#Else, insert new data.
                table.put_item(Item={'instance_id': ec2_instance_info[0],'State_Name': ec2_instance_info[1],'InstanceType': ec2_instance_info[2],'ImageId': ec2_instance_info[3]})

def remove(id):
    try: 
        table.delete_item(Key={'instance_id': id})
        print("Instance record deleted")
    except: print("Instance not found/deleted")

def all():
    db_instance_info = table.scan(('instance_id'))
    results = db_instance_info['Items']
    for item in results:
        for key, value in item.items():
            print (key+': ', value)
        print("-------")

