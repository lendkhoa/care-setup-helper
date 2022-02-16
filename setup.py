"""
Helper to setup or restore postgres database from K8s
for platform, doctor_api & tm_oauth


Author: Khoa Le
Version: Nov 19, 2021
"""

import cprint as p
import subprocess

def setup_platform():
	p.cprint("Setting up platform ...", p.bcolors.WARNING)
	f = open("./locations.txt", "r")
	platform = f.readlines()[0]
	platform_dir = platform[platform.index(":") + 1:]
	platform_dir = platform_dir.strip()
	print(platform_dir)
	changeDir = '(cd ' + platform_dir

	# subprocess.call(changeDir + ' && make setup)', shell=True)

	# maybe skip this step and assume the snap file is already available
	# vault = {'username': 'v-github-l-demo-pla-7ixfuSp3XDpFR7RZCYTO-1638573956', 'password': 'sYqf-TR7dwb7GTTfnEFV'}
	# tmdemo = 'postgresql://' + vault['username'] + '@keeps-doctor-portal-demo.cwatq52g7l69.us-east-2.rds.amazonaws.com:5432/ebdb'
	# tmdemo = 'TMDEMO=' + tmdemo
	# print(tmdemo)
	# subprocess.call(changeDir + ' && ' + tmdemo + ')', shell=True)
	subprocess.call(changeDir + ' && echo $TMDEMO)', shell=True)
	# subprocess.call(changeDir + ' && pg_dump $TMDEMO > test_download.sql)', shell=True)


def vault_access():
	output = subprocess.check_output("vault read -address='https://vault.fortymadison.com' database/creds/demo-platform-read-write", shell=True)
	lines = output.splitlines()
	password = lines[5]
	username = lines[6]
	password = password[password.index('password') + 11 :].strip()
	username = username[username.index('username') + 11 :].strip()
	vault = {
		'username' : username,
		'password' : password
	}
	vault

def main():
	setup_platform()

if __name__ == '__main__':
	main()
