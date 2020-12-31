from flask import Flask, request
import json
from localupdates import pull, posts

app = Flask(__name__)

@app.route('/')
def index():
	return 'Hello World'

@app.route('/', methods=['POST'])
def hook():
	payload = json.loads(request.form['payload'])
	repo_name = payload['repository']['name']
	print(f'Updating {repo_name}')
	print(f'Pulling: {pull(repo_name)}')
	try:
		print(f'Updating logs: {posts(repo_name)}')
	except e as Exception:
		print('Failed to process posts')
	
	return '{"status":"success"}'

if __name__ == "__main__":
	app.run(host='127.0.0.1', port=3002)

