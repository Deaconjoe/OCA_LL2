import sys
import re
import os

print(sys.argv[1])
pick = sys.argv[1]

def GetContainterId(pick):

	my_cmd = 'docker ps'
	cmd_output = str(os.popen(my_cmd).read())
	get_ids = re.findall("[A-Za-z0-9]{12}", cmd_output)
	print('runing containers: '+ str( get_ids))
	print ('connecting to container ' +str(pick) + '... ' )
	return(get_ids[int(pick)])

ContainerId = GetContainterId(pick)

def ConnectToContainer(ContainerId):
	x = ContainerId
	my_cmd = 'docker exec -it ' + x +' /bin/bash'
	cmd_output = os.system(my_cmd)
	
	return('Disconnected from containter ' + str(x))

print(ConnectToContainer(ContainerId))
