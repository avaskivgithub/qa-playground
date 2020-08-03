#!/bin/bash

echo ''
echo 'To start "Test App" run: "bash control.sh"'
echo 'To stop "Test App" run: "bash control.sh stop"'
echo ''

echo 'As a result it would be started / stopped:'
echo 'REST API: http://127.0.0.1:12345/'
echo 'WEB UI: http://127.0.0.1:5000/'

echo ''

control="$1"

app_root_dir='project/app/'
log_dir='/tmp/'

web_gui='web_gui.py'
api='api_server.py'


if [ "$control" = "stop" ]
then

  echo 'Stopping ...'
  for app in $api $web_gui
  do
    kill $(ps aux | grep ${app_root_dir}${app} | grep -v grep | awk '{print $2}')
    echo "Stopped ${app_root_dir}${app}"
  done

else

  echo 'Starting ...'
  for app in $api $web_gui
  do
    nohup python ${app_root_dir}${app} &> ${log_dir}${app}.log &
    echo "Started ${app_root_dir}${app}"
  done

fi
