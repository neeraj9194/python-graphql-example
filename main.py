from ariadne import make_executable_schema
from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from starlette.responses import JSONResponse

from database import create_table

from mutators import mutation
from query import query


app = Starlette(debug=True)


@app.route('/create-table')
async def create_table_api(request):
    res = create_table()
    return JSONResponse({'number_of_items': res})


type_defs = """
    type Query {
        tasks(user_id: String!): [Task]
        users: [User]
    }

    type Mutation {
        user(user_id: String!, name: String!, email: String): User!
        task(user_id: String!, task_id: Int!, desc: String!): Task!
        MarkTaskDone(user_id: String!, task_id: Int!): Boolean!
    }

    type Task {
        task_id: Int!
        desc: String!
        done: Boolean
        user_id: String!
    }

    type User {
        user_id: String!
        name: String!
        email: String
    }
"""

# Create executable schema instance
schema = make_executable_schema(type_defs, query, mutation)
app.mount("/graphql", GraphQL(schema, debug=True))
