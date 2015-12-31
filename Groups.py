## 
## Groups class. 
##	Contains all of the information regarding Groups. 
##

class Group(object):
	def __init__(self, name, message_count, creator_user_id, group_id, id_, users):
		self.name = name
		self.users = users
		self.message_count = message_count
		self.creator_user_id = creator_user_id
		self.group_id = group_id
		self.id_ = id_

	def showName(self):
		return self.name

	def showMessageCount(self):
		return self.message_count

	def showCreatorUserId(self):
		return self.creator_user_id

	def showGroupId(self):
		return self.group_id

	def showId(self):
		return self.id_

	def showMembers(self):
		nickname = self.users.getNickname()
		user_id = self.users.getUserId()
		image_url = self.users.getImageURL()

		## Create list of dicts 
		dictCollection = []
		for nickname, user_id, image_url in zip(nickname, user_id, image_url):
			userDict = {}
			userDict['nickname'] = nickname
			userDict['userId'] = user_id
			userDict['imageUrl'] = image_url
			dictCollection.append(userDict)
		
		return dictCollection

	def numberOfMembers(self):
		number_of_members = len(self.users)
		return number_of_members