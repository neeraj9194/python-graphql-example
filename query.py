from ariadne import QueryType
from boto3.dynamodb.conditions import Key

from database import dynamodb


query = QueryType()


@query.field("tasks")
def resolve_tasks(*_, user_id):
    """
    Resolver for tasks: List of all tasks for a user.
    """
    table = dynamodb.Table('task')
    response = table.query(KeyConditionExpression=Key('user_id').eq(user_id))
    return response['Items']

#
# @query.field("currentUser")
# def resolve_users(*_):
#     """
#     Resolver users: List of all users.
#     """
#     pass

