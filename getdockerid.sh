command_output=$(docker ps) 

if [[ $command_output =~ '[A-Za-z0-9]{12}' ]]; then
	echo $command_output
fi

echo $command_output
