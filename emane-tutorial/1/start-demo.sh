demo_path="/emane-tutorial/1"

mkdir -p $demo_path/persist/$NODE_NO/var/log
mkdir -p $demo_path/persist/$NODE_NO/var/run

echo "im here"
# start emane
emane $demo_path/platform$NODE_NO.xml -r -d -l 3 -f $demo_path/persist/$NODE_NO/var/log/emane.log

# start event daemon
emaneeventd $demo_path/eventdaemon$NODE_NO.xml -r -d -l 4 -f $demo_path/persist/$NODE_NO/var/log/emaneeventd.log
#emaneeventd            eventdaemon$NODE_NO.xml -r -d -l 4 -f            persist/$NODE_NO/var/log/emaneeventd.log

sleep 1
# start gpsd
gpsd -P $demo_path/persist/$NODE_NO/var/run/gpsd.pid -G -n -b $(cat $demo_path/persist/$NODE_NO/var/run/gps.pty)

#start mgen
starttime=
startoption=""
if [ -n "$starttime" ]; then
    startoption="start $(date --date "$starttime" "+%H:%M:%S" --utc)GMT"
fi

mgen input $demo_path/mgen \
     output $demo_path/persist/$NODE_NO/var/log/mgen.out  \
     $startoption
     txlog &> $demo_path/persist/$NODE_NO/var/log/mgen.log &