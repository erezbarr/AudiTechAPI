from flask import Flask, request
from flask_restful import Resource, Api
import requests
import json
import mysql.connector
import threading
from AudiTechGrid.AudiTechGrid import RunGrid as Grid
from AudiTechApi.github_listener.listener import RunListener as Listener


class Pullrequests(Resource):
    def post(self):
        if "New Request" == request.headers.get('PullRequest'):
            response = requests.get('https://api.github.com/repos/erezbarr/auditech/pulls?state=all')
            json_content = json.loads(response.content)
            new_pull_request = json_content[0]
            url = new_pull_request['url']
            id_number = new_pull_request['id']
            number = new_pull_request['number']
            state = new_pull_request['state']
            user = new_pull_request['user']['login']
            title = new_pull_request['title']
            created_at = new_pull_request['created_at']
            mydb = mysql.connector.connect(host="localhost",
                                           user="pullrequestor",
                                           password="password",
                                           database="pullrequests")  # take into account that the DB and table exists
            mycursor = mydb.cursor()
            sql = "INSERT INTO requestsdata (Url, Id, Number, State, User, Title, CreationTime) VALUES (%s, %s, %s, %s, %s, %s, %s);"
            val = (url, id_number, number, state, user, title, created_at)
            mycursor.execute(sql, val)
            grid_thread.start()
            print("New Pull Request - Server")


class ListenerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        listener_instance = Listener()
        listener_instance.run_me()

class GridThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        grid_instance = Grid()
        grid_instance.run_me()

app = Flask(__name__)
api = Api(app)
api.add_resource(Pullrequests, '/pullrequests')  # '/users' is our entry point
listiner_thread = ListenerThread()
grid_thread = GridThread()
if __name__ == "__main__":
    listiner_thread.start()
    app.run()
