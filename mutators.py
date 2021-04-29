from ariadne import MutationType

from database import dynamodb

mutation = MutationType()


@mutation.field("task")
def create_task(_, info, user_id, task_id, desc):
    """
    Add task for a user.
    """
    user_table = dynamodb.Table('user')
    user = user_table.get_item(Key={'user_id': user_id})
    if user.get('Item'):
        table = dynamodb.Table('task')
        table.put_item(
            Item={'user_id': user_id,
                  'task_id': task_id,
                  'desc': desc,
                  'done': False}
        )
        return {'user_id': user_id,
                'task_id': task_id,
                'desc': desc,
                'done': False}
    else:
        return {'task_id': 0, 'desc': "", "error": "User does not exist."}


@mutation.field("user")
def create_user(_, info, user_id, name, email):
    """
    Add a user.
    """
    user_table = dynamodb.Table('user')
    user_table.put_item(Item={'user_id': user_id, 'name': name, 'email': email})
    return {'user_id': user_id, 'name': name, 'email': email}


@mutation.field("MarkTaskDone")
def mark_task_done(_, info, user_id, task_id):
    """
    Mark task as done.
    """
    table = dynamodb.Table('task')
    task = table.get_item(Key={'user_id': user_id, 'task_id': task_id})
    if task.get("Item"):
        table.update_item(Key={'user_id': user_id, 'task_id': task_id},
                          UpdateExpression="set done = :r",
                          ExpressionAttributeValues={
                              ':r': True,
                          })
        return True
    else:
        return False
