import stashy, pprint
from pync import Notifier
from collections import defaultdict
from time import time, sleep
from config import *
if blink:
	from subprocess import call

d = defaultdict(int)
last_updated = int(time()) * 1000

stash = stashy.connect(url, username, password).projects['WT']
Notifier.notify('Now checking for merged pull requests.')
while True:
	try:
		print 'checking: ' + str(last_updated)
		for repo in repos_to_check:
			pull_requests = list(stash.repos[repo].pull_requests.all(state='MERGED', order="NEWEST"))
			if pull_requests:
				pr = pull_requests[0]
				merged_time = pr['updatedDate']
				d[repo] = merged_time
				if merged_time > last_updated:
					Notifier.notify('New pull request merged', title=repo, open=url+'/projects/WT/repos/'+repo+'/pull-requests/'+str(pr['id'])+'/overview')
					if blink:
						call('./blink1-tool --blue', shell=True)
				else:
					print repo + ": no new pull requests merged"
			else:
				print repo + ": no pull requests at all"
		sleep(5)
		if blink:
			call('./blink1-tool --off', shell=True)
		last_updated = int(time()) * 1000
		sleep(20)
	except KeyboardInterrupt:
		exit()