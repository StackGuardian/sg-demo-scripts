import json
from logging import error
import os
import sys

import boto3


def get_env(env_key, default_value="./"):
    env_value = default_value
    if env_key in os.environ:
        env_value = os.getenv(env_key)
    return env_value


def write_outputs_json(key, value):
    artifactsDir = get_env("LOCAL_ARTIFACTS_DIR")

    jsonOut = {
        key: {
            "type": "string",
            "value": value,
            "sensitive": False,
        }
    }

    with open(f"{artifactsDir}/sg.outputs.json", "w+") as file:
        json.dump(jsonOut, file, skipkeys=False, indent=2)


def check_aws_variables():
    # Check if AWS_DEFAULT_REGION is set in the environment variables
    if "AWS_DEFAULT_REGION" not in os.environ:
        # If not, show error and exit with 1
        error("AWS_DEFAULT_REGION is not set in the environment variables.")
        exit(1)


def find_ec2_instances_by_tag(tag_key, tag_value):
    # Create an EC2 client
    ec2 = boto3.client("ec2")

    # Prepare the filter for the tag
    filters = [{"Name": f"tag:{tag_key}", "Values": [tag_value]}]

    # Fetch instance details
    response = ec2.describe_instances(Filters=filters)

    instance_list = []

    # Loop over instance details and format output
    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", {}):
            instance_id = instance.get("InstanceId")
            instance_public_ip = instance.get(
                "PublicIpAddress", "Public IP not assigned"
            )

            instance_data = {
                "id": instance_id,
                "public_ip": instance_public_ip,
            }
            instance_list.append(instance_data)

    return instance_list


def main():
    if len(sys.argv) != 2:
        error("Usage: python get_ec2_instance_output.py <tag_value>")
        exit(1)

    # Default tag values
    tag_key = "Name"
    tag_value = sys.argv[1]

    # check_aws_variables()
    instance_list = find_ec2_instances_by_tag(tag_key, tag_value)

    if instance_list:
        instance_ids = [instance.get("id") for instance in instance_list]
        print("Instances found:", instance_ids)
        print("Using first instance:", instance_ids[0])

        print("Writing outputs to sg.outputs.json")
        write_outputs_json(tag_value, instance_list[0]["public_ip"])
    else:
        print(f"No instances found with the tag ({tag_key}:{tag_value}).")


if __name__ == "__main__":
    main()
