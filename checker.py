import stashy, pprint
from collections import defaultdict
from time import time, sleep
from subprocess import call
from config import *

d = defaultdict(int)
last_updated = int(time()) * 1000

stash = stashy.connect("http://www-git.server.gvsu.edu:7990", username, password).projects['WT']

while True:
	try:
		print 'checking: ' + str(last_updated)
		for repo in repos_to_check:
			pull_requests = list(stash.repos[repo].pull_requests.all(state='MERGED', order="NEWEST"))
			if pull_requests:
				merged_time = pull_requests[0]['updatedDate']
				d[repo] = merged_time
				if merged_time > last_updated:
					print repo + ': new pull request merged'
					call('blink1-tool --blue', shell=True)
				else:
					print repo + ": no new pull requests merged"
			else:
				print repo + ": no pull requests at all"
		sleep(5)
		call('blink1-tool --off', shell=True)
		last_updated = int(time()) * 1000
		sleep(20)
	except KeyboardInterrupt:
		exit()