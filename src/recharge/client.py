import requests
import json

class Recharge:
	def __init__(self,key):
		self.api_key = key
	def headers(self):
		return {
			"X-Recharge-Version": "2021-11",
			"Content-Type": "application/json",
			"X-Recharge-Access-Token": self.api_key
		}
	def url(self,url): 
		return "https://api.rechargeapps.com/%s" % (url)
	def get(self,url):
		return requests.get(self.url(url),headers=self.headers()).json()
	def get_all(self,url,record_type=""):
		proceed = True
		cursor = ""
		ret = []
		while proceed:
			query = f"{url}&limit=250"
			if cursor:
				query = f"{url.split('?')[0]}?limit=250&cursor={cursor}"
			subs = self.get(query)
			for sub in subs.get(record_type,[]):
				ret.append(sub)
			if "next_cursor" in subs and subs["next_cursor"]is not None:
				cursor = subs["next_cursor"]
			else:
				proceed = False
		return ret
			
	def post(self,url,body={}):
		return requests.post(self.url(url),data=json.dumps(body),headers=self.headers()).json()
	def put(self,url,body={}):
		return requests.put(self.url(url),data=json.dumps(body),headers=self.headers()).json()
	def delete(self,url):
		return requests.delete(self.url(url),headers=self.headers()).status_code

class RechargeRecord(Recharge):
    def __init__(self,type,payload):
        self.type = type;
        self.payload = payload
        self.id = payload.get("id")
    def delete(self):
        return super.delete(f"{type}/{self.id}")
    def update(self,payload):
        return super.put(f"{self.type}/{self.id}",payload)
    