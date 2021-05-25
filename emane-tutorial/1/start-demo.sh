mkdir -p persist/$NODE_NO/var/log
mkdir -p persist/$NODE_NO/var/run

# start emane
emane platform$NODE_NO.xml -r -d -l 3 -f persist/$NODE_NO/var/log/emane.log

# start event daemon
emaneeventd eventdaemon$NODE_NO.xml -r -d -l 4 -f persist/$NODE_NO/var/log/emaneeventd.log

sleep 1
# start gpsd
gpsd -G -n -b $(cat persist/$NODE_NO/var/run/gps.pty)