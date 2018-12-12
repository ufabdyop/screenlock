import sys, requests

def main():
	num = len(sys.argv)
	if num < 3:
		print("Please enter at least two arguments")
		print("eg. commandClient.exe https://localhost:9092 admin 1234 status")
		print("eg. commandClient.exe https://localhost:9092 admin 1234 lock")
		print("eg. commandClient.exe https://localhost:9092 admin 1234 unlock")
		print("eg. commandClient.exe https://localhost:9092 version")
		sys.exit(0)
	else:
		mainUrl = sys.argv[1]
		path = sys.argv[2]
		url = mainUrl + '/' + path
		username = None
		psw = None
		response = None
		try:
			if num == 5:
				path = sys.argv[4]
				url = mainUrl + '/' + path
				username = sys.argv[2]
				psw = sys.argv[3]
				if path == 'lock':
					response = requests.post(url, auth = (username,psw),verify = False, data = {"submit": "Lock the Screen"})
				elif path == 'unlock':
					response = requests.post(url, auth = (username,psw),verify = False, data = {"submit": "Unlock the Screen"})				
				elif path == 'status':
					response = requests.get(url, auth = (username, psw), verify = False)
			elif path == 'version':
				response = requests.get(url, verify = False)
			else:
				print("Incorrect arguments")
				sys.exit(0)
			if response is not None:
				if str(response.status_code) == '200':
					print(response.text)
				else:
					print(response.status_code)
		except Exception as err:
			print ('Exception: ' + str(err))


if __name__ == '__main__':
	main()

