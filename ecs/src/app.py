import os
import boto3

ecs = boto3.client("ecs")

def auto_stop_ecs_handler(event, context):
    print("Stop ECS Task")
    clusters = ecs.list_clusters()
    for cls in clusters['clusterArns']:
        services = ecs.list_services(cluster=cls)
        describe_services = ecs.describe_services(cluster=cls, services=services['serviceArns'])
        for service in describe_services['services']:
            response = ecs.update_service(
                cluster=service['clusterArn'], 
                service=service['serviceName'], 
                desiredCount=0,
                taskDefinition=service['taskDefinition'], 
                forceNewDeployment=True
            )
            print("Stop task: {} in service: {}".format(response['service']['taskDefinition'], response['service']['serviceName']))

def auto_start_ecs_handler(event, context):
    print("Start ECS Task")
    clusters = ecs.list_clusters()
    running_count = os.getenv("RUNNING_COUNT")
    for cls in clusters['clusterArns']:
        services = ecs.list_services(cluster=cls)
        describe_services = ecs.describe_services(cluster=cls, services=services['serviceArns'])
        for service in describe_services['services']:
            response = ecs.update_service(
                cluster=service['clusterArn'], 
                service=service['serviceName'], 
                desiredCount=int(running_count),
                taskDefinition=service['taskDefinition'], forceNewDeployment=True
            )
            print("Start task: {} with count {} in service: {}".format(response['service']['taskDefinition'], running_count, response['service']['serviceName']))

if __name__ == "__main__":
    auto_stop_ecs_handler(None, None)
    # auto_start_ecs_handler(None, None)
