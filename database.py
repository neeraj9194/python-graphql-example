import boto3

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://db:8000',
    region_name='eu-west-1'
)


# Create the DynamoDB table.
def create_table():
    user = dynamodb.create_table(
        TableName='user',
        KeySchema=[
            {
                'AttributeName': 'user_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'user_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        },
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'user_',
                'KeySchema': [
                    {
                        'AttributeName': 'string',
                        'KeyType': 'HASH'
                    },
                ],
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            }
        ]
    )

    task = dynamodb.create_table(
        TableName='task',
        KeySchema=[
            {
                'AttributeName': 'user_id',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'task_id',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'user_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'task_id',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Wait until the table exists.
    task.meta.client.get_waiter('table_exists').wait(TableName='user')
    user.meta.client.get_waiter('table_exists').wait(TableName='task')
    return task.item_count + user.item_count
