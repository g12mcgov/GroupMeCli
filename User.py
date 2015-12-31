## 
## User class. 
##	Contains all of the information regarding Users. 
##

class User:
	def __init__(self, nickname, user_id, image_url):
		self.nickname = nickname
		self.user_id = user_id
		self.image_url = image_url

	def getNickname(self):
		return self.nickname

	def getUserId(self):
		return self.user_id

	def getImageURL(self):
		return self.image_url

