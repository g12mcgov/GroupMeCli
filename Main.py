##
## GroupMeCli - An open source command line client for the GroupMe messaging app.
##
## Created by: Grant McGovern
## Date: 31 July 2014
## Contact: github.com/g12mcgov
##
## Purpose: To provide a command line tool to be used to send/recieve/favorite/and view
## GroupMe chats/groups. For those of us who are always in front of a shell and want to stay
## in the loop... [see Github page for more info]
##
##
##

import csv
import json
import requests
from User import *
from Groups import *
from random import randint
from termcolor import colored
from prettytable import PrettyTable
import Completer
import readline

comp = Completer.Completer()
print comp.complete_list
readline.parse_and_bind("tab: complete")
readline.set_completer(comp.complete)

## The core url of GroupMe's API
base_url = "https://api.groupme.com/v3"

def main():
	global ACCESS_KEY
	ACCESS_KEY = getKey()

	print "Welcome to GroupMe Cli, a brief command line client for GroupMe.\n"
	print 'Type "help" at any point to view the Display Options again.'
	print "The groups you belong to are listed below:\n"
	users = aggregateFetch()
	displayOptions()

	while True:
		response = raw_input('> ')
                #remove ending whitespace
                response = response.strip()
		if response == 'help':
			displayOptions()
		elif response == '1':
			aggregateFetch()
			displayOptions()
		elif response == '2':
			displayOptions()
		elif response == '3':
			print "\nEnter your groupId"
			print "Don't know it? Type %s\n" % colored("find", 'green')

			while True:
				user_input = raw_input('> ')
				user_input = user_input.strip()

				if user_input == 'find':
					titles = findGroups()
					for title in titles:
						print title
					print "\n"
				elif user_input == 'menu':
					displayOptions()
					break
				elif user_input == 'exit':
					return
                                elif user_input == 'back':
                                        break
				else:
					while True:
						groupID = user_input
						try:
							viewMessages(base_url+'/groups/', groupID, users)
                                                except:
                                                        print "Failed to load messages"
                                                        break
						response = messagePrompt(groupID)
						if response == None:
							displayOptions()
							break
						elif response == 'like':
							messageId = raw_input('Please enter messageID > ')
							favoriteMessage(groupID, messageId)
						elif response == 'unlike':
							messageId = raw_input('Please enter messageID > ')
							unfavoriteMessage(groupID, messageId)
						elif response == 'back':
                                                        comp.clear_complete_list()
							break ## Go back to menu level
						elif response == 'exit':
							return ## Exit out of entire program
						elif response == 'refresh':
							viewMessages(base_url+'groups/', groupID, users)
						elif response:
							sendMessageToGroup(response, groupID)
                                                else:
							print "Invalid input."
					if response == 'no':
						break
		elif response == "exit":
			return
		else:
			print "Not a valid selection"

def displayOptions():
	print "\nPlease select what to do: \n"
	print "1) View Joined Groups"
	print "2) Send Message"
	print "3) Chat with Group"
	print 'Type %s to quit' % colored("exit", 'red', attrs=['bold','blink'])
	print "\n"

def messagePrompt(groupID):
	#print "Do you want to send a message? (y/N)"
	print "Note: you can always type %s or %s to favorite a message. You can also refresh the chat with %s or '%s'." % (colored("like", 'green', attrs=['bold']), colored("unlike", 'red', attrs=['bold']), colored("refresh", 'green', attrs=['bold']), colored("r", 'green', attrs=['bold']))
	response = raw_input('Type a message > ')
	if response == 'exit':
		return "exit"
	elif response == None:
		return None
	elif response == 'like':
		return "like"
	elif response == 'unlike':
		return "unlike"
	elif (response == 'refresh') or (response == 'r'):
		return "refresh"
	elif response == 'back':
		return "back"
	elif response:
		return response
	else:
		print "Not valid input"


def aggregateFetch():
	users = []
	Groups = getGroups(base_url+'/groups')
	for group in Groups:
		dictCollection = showGroups(group)
		users.append(fetchUsers(dictCollection))

	return users

def findGroups():
	titles = []
        group_ids = []
	Groups = getGroups(base_url+'/groups')
	for group in Groups:
		name = group.showName()
		group_id = group.showGroupId()
                group_ids.append(group_id)
		groupId = colored("Group ID:", 'yellow')
		title = "Name: %s | %s " % (colored(name, 'green'), group_id)
		titles.append(title)
        comp.set_complete_list(group_ids)
	return titles

def getGroups(base_url):
	print "Fetching groups...\n"
	req = requests.get(url=base_url+"?", params={'token':ACCESS_KEY})
	print req.url

	data = json.loads(req.content)

	## For debug purposes, so we can view what we're getting (prettily)
	json_response = json.dumps(data, ensure_ascii=False, encoding="utf-8", separators=(',', ':'), indent=4)

	## Checks for authentication/existence of developer key.
	try:
		errors = data["meta"]["errors"]
		if errors:
			for error in errors:
				if "UnauthorizedError" in error:
					print colored("Please check you have loaded your Developer key.", 'red')
	except:
		pass

	responses = data["response"]

	names = [name["name"] for name in responses]
	ids = [id_["id"] for id_ in responses]
	messageCounts = [message_count["messages"]["count"] for message_count in responses]
	groupids = [group_id["group_id"] for group_id in responses]
	creatorUserIds = [creator_user_id["creator_user_id"] for creator_user_id in responses]
	member_blocks = [member["members"] for member in responses]

	userIds = []
	nicknames = []
	imageUrls = []

	userIds = [[user_id["user_id"] for user_id in block] for block in member_blocks]
	nicknames = [[nickname["nickname"] for nickname in block] for block in member_blocks]
	imageUrls = [[image_url["image_url"] for image_url in block] for block in member_blocks]

	Groups = []
	Users = []

	for nickname, user_id, image_url in zip(nicknames, userIds, imageUrls):
		Users.append(User(nickname, user_id, image_url))

	for name, message_count, creator_user_id, group_id, id_, user in zip(names, messageCounts, ids, groupids, creatorUserIds, Users):
		Groups.append(Group(name, message_count, creator_user_id, group_id, id_, user))

	return Groups

def showGroups(group):
	name = group.showName()
	message_count = group.showMessageCount()
	creator_user_id = group.showCreatorUserId()
	group_id = group.showGroupId()
	id_ = group.showId()

	dictCollection = group.showMembers()

	messageCount = colored("Message Count:", 'yellow')
	creator = colored("Creator:", 'yellow')
	groupId = colored("Group ID:", 'yellow')
	ID = colored("ID:", 'yellow')

	users = fetchUsers(dictCollection)

	title = "%s | %s %s | %s %s | %s %s | %s %s |" % (colored(name, 'green'), messageCount, message_count, creator, creator_user_id, groupId, group_id, ID, id_)

	table = PrettyTable([title, "User ID"])
	table.align[title] = "l" ## Align title to the left
	table.padding_width = 1
	table.add_row(["Members:", ""])
	table.add_row(["", ""])
	for user in users:
		table.add_row([user[2], user[0]])

	print table

	return dictCollection

def fetchUsers(dictCollection):
	users = []
	for userDict in dictCollection:
		user = tuple(userDict.values())
		users.append(user)

	return users

def lookupUser(users, userId):
	for user in users:
		for userTuple in user:
			if userTuple[0] == userId:
				return userTuple[2] ## Grab the username for a userID

def viewMessages(url, groupID, users):
	print "Loading messages..."
        message_ids = []
	endpoint = url + groupID + '/messages'
        
	#data = requests.get(url=endpoint, params={'token':ACCESS_KEY, 'limit':30})

	data = json.loads(requests.get(url=endpoint, params={'token':ACCESS_KEY, 'limit':30}).content)

	messages = data["response"]["messages"]
	#print json.dumps(messages, indent=4, separators=(',', ':'))

	names = [name["name"] for name in messages]
	texts = [text["text"] for text in messages]
	favorites = [favorite["favorited_by"] for favorite in messages]
	attachments = [attachment["attachments"] for attachment in messages]
	messageIds = [messageId["id"] for messageId in messages]

	heart = u'\u2764'
	heart = colored(heart.encode('utf-8'), 'red')

	dictCollection = []

	for name, text, favorite, attachment, messageId in reversed(zip(names, texts, favorites, attachments, messageIds)):
		message = {}
		message['name'] = name
		message['text'] = text
		message['favorite'] = [lookupUser(users, fav) for fav in favorite] ## List object
		message['id'] = messageId
                message_ids.append(messageId)
		message['attachment'] = attachment
		dictCollection.append(message)

	for messageDict in dictCollection:
		if messageDict['favorite']:
			print "%s: %s %s : %s" % (colored(messageDict['name'], 'yellow'), messageDict['text'], unicode(heart, 'utf-8'), messageDict['favorite'])
			print "id: %s\n" % colored(messageDict['id'], 'cyan')
		else:
			print "%s: %s" % (colored(messageDict['name'], 'yellow'), messageDict['text'])
			print "id: %s\n" % colored(messageDict['id'], 'cyan')

        comp.set_complete_list(message_ids)

def sendMessageToGroup(message, groupId):
	url = base_url + '/groups/' + groupId + "/messages"

	headers = {"Content-Type":"application/json"}
	## GroupMe has a weird post API feature where you must include a "Source Guid"
	## Unfortunately, they use this as a way to detect multiple messages from the same
	## source. If you send more than a couple messages within a short amount of time, it
	## will temporarily lock you out. To counter this, we can generate a random GUID. Of
	## course, the chance there is a collision still exists, but it is low considering our
	## range of 0 to 1000.
	try:
		payload = {"message":{"source_guid":str(randint(0,1000)),"text":message, "attachments":[]}}

		data = json.loads(requests.post(url=url, headers=headers, data=json.dumps(payload), params={'token':ACCESS_KEY}).content)

		body = data["response"]

		## A simple way to verify if the message was actually sent
		if body["message"]:
			print "Message sent."
	except:
		print "Failed to send."

def favoriteMessage(groupID, messageId):
	url = base_url + '/messages/' + groupID + '/' + messageId + '/like'
	print url

	headers = {"Content-Type":"application/json"}

	response = json.loads(requests.post(url=url, headers=headers, params={'token':ACCESS_KEY}).content)

	print response

def unfavoriteMessage(groupID, messageId):
	url = base_url + '/messages/' + groupID + '/' + messageId + '/unlike'

	headers={"Content-Type":"application/json"}

	response = json.loads(requests.post(url=url, headers=headers, params={'token':ACCESS_KEY}).content)

	print response


def getKey():
	with open("key.csv", 'r') as keyfile:
		keyreader = csv.reader(keyfile)
		for row in keyreader:
			return str(row[0])

if __name__ == "__main__":
	main()
