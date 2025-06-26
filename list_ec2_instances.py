from logging import error
import os

import boto3


def check_aws_variables():
    # Check if neccessary AWS variables are exported to the OS environment
    if not (
        os.getenv("AWS_ACCESS_KEY_ID")
        and os.getenv("AWS_SECRET_ACCESS_KEY")
        and os.getenv("AWS_DEFAULT_REGION")
    ):
        # If not, show error and exit with 1
        error(
            "One of the AWS environment variables is not set."
            + " Please select configured AWS connector to pass variables."
        )
        exit(1)


def list_ec2_instances():
    # Create an EC2 client
    ec2 = boto3.client("ec2")

    # Fetch instance details
    response = ec2.describe_instances()

    # Loop over instance details and format output
    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            print(f"Instance ID: {instance.get('InstanceId')}")
            print(f"Instance Type: {instance.get('InstanceType')}")
            print(f"State: {instance.get('State', {}).get('Name')}")

            if "Tags" in instance:
                print("Tags:")
                for tag in instance["Tags"]:
                    print(f" > {tag.get('Key')}: {tag.get('Value')}")

            print("---")


def main():
    # check_aws_variables()
    list_ec2_instances()


if __name__ == "__main__":
    main()
