#!/bin/sh
echo "Booting rabbitmq server"
sudo rabbitmq-server &
sleep 5
echo "Loading WebReader.py.sh"
./WebReader.py.sh 2 >> ../logs/WebReader.txt &
echo "Loading Organizer.py.sh"
./Organizer.py.sh 5 >> ../logs/Organizer.txt &
echo "Loading URLPicker.py.sh"
./URLPicker.py.sh 2 >> ../logs/URLPicker.txt &
echo "Loading Ranker.py.sh"
./Ranker.py.sh 2 >> ../logs/Ranker.txt &
echo "Sending out first url info"
./send.py.sh >> ../logs/send.py &
