import boto3
import requests
import os
import time

S3_BUCKET = os.environ.get('S3_BUCKET_NAME')
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:5000/api/tasks')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

s3 = boto3.client('s3', region_name='us-east-1')
sns = boto3.client('sns', region_name='us-east-1')


def backup_tasks():
    response = requests.get(BACKEND_URL)
    tasks = response.json()

    with open('backup.txt', 'w') as f:
        for task in tasks:
            f.write(f"- {task['task_name']}\n")

    s3.upload_file('backup.txt', S3_BUCKET, 'task_backup.txt')

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message='Tasks have been successfully backed up to S3!',
        Subject='To-Do App Backup Alert'
    )
    print("Backup completed and alert sent!")


if __name__ == "__main__":
    while True:
        backup_tasks()
        time.sleep(3600)  # Runs every hour
