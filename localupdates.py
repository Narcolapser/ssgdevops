import sys
import json
from git import Repo

time_str = '%Y-%m-%d'
my_names = ['Toben Archer','Narcolapser','Toben']

def pull(repo_name):
	repo_path = f'/home/toben/Code/ssg/{repo_name}'
	repo = Repo(repo_path)

	if repo.active_branch.name != 'master':
		print('Unable to update as the active branch is not currently the master branch.')
		return False

	remote_name = 'origin'

	remote = None
	for r in repo.remotes:
		if r.name == remote_name:
			remote = r
			break

	if not remote:
		print(f'Unable to update as no remote "{remote_name}" was found')
		return False

	try:
		remote.pull()
	except Exception as e:
		print(f'Unable to update due to a {type(e)}: {e}')
		return False
	
	return True

def posts(repo_name):
	repo_path = f'/home/toben/Code/ssg/{repo_name}'
	repo = Repo(repo_path)

	posts = []
	for commit in repo.iter_commits('master'):
		if commit.author.name not in my_names:
			continue
		lines = commit.message.split('\n')
		title = lines[0]
		if len(lines) > 2:
			body = '\n'.join(lines[2:])
			
			body = body.replace('\n\n','LINEBREAK')
			body = body.replace('\n',' ')
			body = body.replace('LINEBREAK','\n\n')
		else:
			body = title
		posts.append({'title':title,
					  'message':body,
					  'project':repo_name,
					  'author':commit.author.name,
					  'date':commit.committed_datetime.strftime(time_str),
					  'branch':'master'
					  })


	logs = {'name':'',
			'description':'',
			'url':'',
			'rank':'',
			'files':'',
			'path':'',
			'posts':posts}
	
	log_file = open(f'{repo_path}/logs.json','w')
	json.dump(logs,log_file)
	log_file.close()
	return True
