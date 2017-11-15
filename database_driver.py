# Nicolas Flores and Shaket Chaudhary
# CS 61
# Lab 3 part B

from __future__ import print_function
import pymongo
from database_functions import *


HOST = "mongodb://Team29:lp0Xr2HdnHxcK0ZO@cluster0-shard-00-00-ppp7l.mongodb.net:27017,cluster0-shard-00-01-ppp7l.mongodb.net:27017,cluster0-shard-00-02-ppp7l.mongodb.net:27017/Team29DB?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin"
DB_NAME = "Team29DB"
if __name__ == "__main__":

    # Connect to Atlas and then our database (Team29DB)
    client = pymongo.MongoClient(HOST)
    db = client[DB_NAME]

    print("Connection to Atlas established.\n")

    INPUT = greet()

    while INPUT != 'quit':

        if INPUT == 'post':
            handlePost(db)
        elif INPUT == 'comment':
            handleComment(db)
        elif INPUT == 'delete':
            handleDelete(db)
        elif INPUT == 'show':
            handleShow(db)
        # Developer functions:
        elif INPUT == 'print':
            handlePrint(db)
        else:
            handleIncorrectInput(db)

        INPUT = greet()

    print("Connection terminated.\n")