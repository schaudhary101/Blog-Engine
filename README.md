# Shaket Chaudhary and Nicolas Flores
# CS 61 Lab 2b
# November 13, 2017


## Setup

To run, you want to make sure at least the two files are in the same directory:
	*database_driver.py*
	*database_functions.py*
Additionally, you may want to use test1.in which is what we used to test our files.

To run, you may use either Pycharm or Terminal which we recommend. 
The command we used: *python database_driver.py*

## Functions

We had 4 main functions that we implemented in this lab.

	post

After selecting this option, the user must specify in the following order:

	blogName userName title postBody tags

The function then either creates a new blog or posts in an existing blog.
An entryID is generated and is unique for each post. Tags is an optional parameter.

	comment

After selecting this option, the user must specify in the following order:

	blogName entryID userName commentBody

We decided to implement comments as their own documents, their parent is stored
as a parentID, and thus this allows for commenting on comments as well.

	delete

After selecting this option, the user must specify in the following order:

	blogName entryID userName

To delete, the user must be the author of the post, otherwise they are denied.
Additionally, a deleted page keeps its entryID, and it's parentID if it is a comment.
However, the remaining content is replaced with a deleted message. A user cannot delete
a page that already has been deleted.

	show

After selecting this option, the user must specify in the following order:

	blogName

The function then prints tabs and retrieves the information, 
a comment on a post or a comment will be indented.