from __future__ import print_function
from pprint import pprint
import datetime
import shlex

# Used in the main to greet the user and retrieve input; Also allows the user to type 'POST' or 'pOsT' instead of 'post'
def greet():
    print("Please input a request:")
    print("Options: post, comment, delete, show")
    print("Or type 'quit' to quit\n")
    userInput = raw_input(">")
    print("")
    userInput = userInput.lower()
    userInput = userInput.strip()

    return userInput

# Checks if the blog exists
def doesBlogExist(db, blogName):
    if blogName not in db.collection_names():
        return False
    else:
        return True


# Checks if their exists a post by that entryID
def doesPostExist(db, blogName, entryID):
    maxID = findNewEntryID(db, blogName) - 1
    if int(entryID) > int(maxID):
        return False
    else:
        return True


# Checks if a post has a 'deleted' field
def isPostDeleted(db, blogName, entryID):
    post = db[blogName].find_one({"entryID": entryID})

    if "deleted" in post:
        return True
    else:
        return False


# Checks to make sure that an entryID is an integer
def isDigit(entryID):
    try:
        int(entryID)
        return True
    except ValueError:
        return False


# Retrieves input in a standardized manner
def inputToShlexArray():
    rawInput = raw_input(">")
    userInput = shlex.split(rawInput)

    return userInput

# Relic of trying to remove quotes, before shlex
def removeQuotesIfQuotes(s):
    if s[0] == '"' and s[-1] == '"':
        return s[1:-1]

    if s[0] == "'" and s[-1] == "'":
        return s[1:-1]

    return s


# Finds the highest entryID in the blog and returns 1 more
def findNewEntryID(db, blogName):
    if db[blogName].count() == 0:
        entryID = 1
    else:
        entryArray = list()
        for blogPost in db[blogName].find():
            entryArray.append(blogPost['entryID'])

        entryID = max(entryArray) + 1

    return entryID


# Developer function: print the contents of a blog, sans format
def handlePrint(db):
    userInput = raw_input('>')
    userInput = userInput.strip()

    for blogPost in db[userInput].find():
        pprint(blogPost)


# If the user wants to post a new blog post
def handlePost(db):
    print("Please enter input delimited by spaces in the following format:")
    print("Make sure to group your title, postBody and tags are within quotes, either single or double")
    print("<blogName> <userName> '<title>' '<postBody>' '<tags>'")
    print("Or type 'quit' to quit")
    print("note: tags are optional and separated by commas\n")

    userInput = inputToShlexArray()
    if len(userInput) == 1 and userInput[0] == 'quit':
        return

    # If the format doesn't match the specified format
    if len(userInput) < 4 or len(userInput) > 5:
        handleIncorrectInput(db, True)
        return

    # For easier reference
    blogName = userInput[0]
    userName = userInput[1]
    title = userInput[2]
    postBody = userInput[3]
    tags = userInput[4]
      
    # Check if their is a blog by that blogName, if DNE then make it
    if not doesBlogExist(db, blogName):
        db.create_collection(blogName)

    # Find the proper entryID
    entryID = findNewEntryID(db, blogName)

    # Create the post
    post = {
        "entryID" : entryID,
        "title" : title,
        "username" : userName,
        "tags" : tags,
        "body" : postBody
    }

    db[blogName].insert_one(post)


# If the user wants to post a comment
def handleComment(db):
    print("Please enter input delimited by spaces in the following format:")
    print("Please make sure to encapsulate your comment body within quotes, either single or double")
    print("<blogName> <entryID> <userName> '<commentBody>'")
    print("Or type 'quit' to quit\n")

    text = inputToShlexArray()
    if len(text) == 1 and text == 'quit':
        return

    # If the format does not match the specified format
    if len(text) != 4:
        handleIncorrectInput(db, True)
        return

    # For easier reference
    blogName = text[0]
    entryID = text[1]
    userName = text[2]
    commentBody = text[3]

    # Is the entry ID a number?
    if not isDigit(entryID):
        print("The post/comment you are referencing must be referred to by their entry ID")
        return
    else:
        entryID = int(entryID)

    # Does the blog exist
    if not doesBlogExist(db, blogName):
        print("Unfortunately, the blog you entered does not exist.\n")
        return

    # Does the post exist
    if not doesPostExist(db, blogName, int(entryID)):
        print("Unfortunately, the post you entered does not exist in that blog.\n")
        return

    # You cannot comment on a post that has been deleted
    if isPostDeleted(db, blogName, int(entryID)):
        print("Unfortunately, you cannot make new comments on a deleted post.\n")
        return

    # Find the entryID for the comment document
    newEntryID = findNewEntryID(db, blogName)

    comment = {
        "entryID": newEntryID,
        "parentID": entryID,
        "username": userName,
        "comment": commentBody
    }

    db[blogName].insert_one(comment)


# If the user wants to delete a post
def handleDelete(db):
    print("Please enter the input delimited by spaces in the following format:")
    print("<blogName> <entryID> <userName>")
    print("Or type 'quit' to quit\n")

    userInput = inputToShlexArray()
    if len(userInput) == 1 and userInput[0] == 'quit':
        return

    # If the format doesn't match the specified format
    if len(userInput) != 3:
        handleIncorrectInput(db, True)
        return

    # For easier reference
    blogName = userInput[0]
    entryID = userInput[1]
    userName = userInput[2]

    # Is the entry ID a number?
    if not isDigit(entryID):
        print("The post/comment you are referencing must be referred to by their entry ID")
        return
    else:
        entryID = int(entryID)

    # Check if blog exists
    if not doesBlogExist(db, blogName):
        print("Unfortunately, the blog you entered does not exist.\n")
        return

    # Check if post/comment exists
    if not doesPostExist(db, blogName, int(entryID)):
        print("Unfortunately, the post you entered does not exist in that blog.\n")
        return

    # Has the post been deleted?
    if isPostDeleted(db, blogName, int(entryID)):
        print("Unfortunately, this post has already been deleted.\n")
        return

    # Check if userName matches the post/comment field
    post = db[blogName].find_one({"entryID": int(entryID)})
    if post["username"] != userName:
        print("Unfortunately, you are not the author of this post.\n")
        return
    
    # Create a new document to replace the original content
    message = "deleted by " + userName + " on " + str(datetime.datetime.now())
    
    # Check if it is a comment we are trying to delete; then delete it
    if "parentID" in post:
        parentID = post["parentID"]
        db[blogName].replace_one(
           {"entryID":int(entryID)},
           {"entryID":int(entryID),
           "parentID":int(parentID),
           "deleted":message})
    else:
        db[blogName].replace_one(
           {"entryID":int(entryID)},
           {"entryID":int(entryID),
           "deleted":message})

# If the user wants to show the formatted contents of a blog
def handleShow(db):
    print('Please enter the name of the blog you want to show')
    print("Or type 'quit' to quit\n")

    userInput = inputToShlexArray()

    if len(userInput) == 1 and userInput[0] == 'quit':
        return

    # If the format doesn't match the specified format
    if len(userInput) > 1:
        handleIncorrectInput(db, True)
        return

    blogName = userInput[0]

    # Check if the blog exists
    if not doesBlogExist(db, blogName):
        print("Unfortunately, the blog you entered does not exist.\n")
        return

    # Else blog does exist, show all contents:
    print("Here are the contents of the blog '" + blogName + "':\n")

    if db[blogName].count() == 0:
        print("There is nothing here yet.\n")

    posts = list()
    commentTree = dict()

    # Put all the posts in a list
    # Put all comments in a map, where their key is the ID of their parent
    # Print all the posts, if it has a comment post all of those, if those have comments, post those, etc.
    for blogPost in db[blogName].find():
        if 'parentID' not in blogPost:
            posts.append(blogPost)
        else:
            if not commentTree.has_key(blogPost['parentID']):
                commentTree[blogPost['parentID']] = list()

            commentTree[blogPost['parentID']].append(blogPost)

    for post in posts:
        printBlogPost(db, post, blogName)
        printComments(db, post, commentTree, 1, blogName)

    print("")


# Prints comments recursively for a post
def printComments(db, post, commentTree, level, blogName):
    if commentTree.has_key(post['entryID']):
        for post in commentTree[post['entryID']]:
            printBlogComment(db, post, blogName, level)
            printComments(db, post, commentTree, level+1, blogName)


# Prints formatted blog posts
def printBlogPost(db, blogPost, blogName):
    if isPostDeleted(db, blogName, blogPost['entryID']):
        entryID = blogPost['entryID']
        body = blogPost['deleted']
        print ("(" + str(entryID) + ") ")
        print(body)
    else:
        entryID = blogPost['entryID']
        username = blogPost['username']
        title = blogPost['title']
        body = blogPost['body']
        tags = blogPost['tags']

        print("(" +  str(entryID) + ") " + title)
        print(username)
        print("tags: " + tags)
        print(body)


# Prints formatted blog comments
def printBlogComment(db, blogComment, blogName, level):
    if isPostDeleted(db, blogName, blogComment['entryID']):
        entryID = blogComment['entryID']
        body = blogComment['deleted']

        printToLevel(level)
        print("(" + str(entryID) + ") ")
        printToLevel(level)
        print (body)

    else:
        entryID = blogComment['entryID']
        username = blogComment['username']
        body = blogComment['comment']

        printToLevel(level)
        print("(" + str(entryID) + ") " + username)
        printToLevel(level)
        print(body)


# Adds the appropriate number of tabs to the output for comments
def printToLevel(level):
    for i in xrange(level):
        print('\t', end='')


# If the user messes up
def handleIncorrectInput(db, format):
    if format:
        print ("The input that you have entered is in the incorrect format.\n")
    else:
        print("The input that you have entered is incorrect.\n")
