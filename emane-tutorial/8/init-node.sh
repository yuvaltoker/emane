
demo_path="/emane-tutorial/8"

if [ "$is_probe_testing" = "true" ]; then

#    cd /opentestpoint-probe-emane && \
#    ./autogen.sh && \
#    ./configure && \
#    make && \
#    make deb

#    cd /opentestpoint-probe-emane/.debbuild && \
#    dpkg -i *.deb

#    cd /
fi

rm -r $demo_path/persist/$NODE_NO/var
mkdir -p $demo_path/persist/$NODE_NO/var/log
mkdir -p $demo_path/persist/$NODE_NO/var/run

# start emane
emane $demo_path/platform$NODE_NO.xml -r -d -l 3 -f $demo_path/persist/$NODE_NO/var/log/emane.log

# start event daemon
emaneeventd $demo_path/eventdaemon$NODE_NO.xml -r -d -l 4 -f $demo_path/persist/$NODE_NO/var/log/emaneeventd.log
#emaneeventd            eventdaemon$NODE_NO.xml -r -d -l 4 -f            persist/$NODE_NO/var/log/emaneeventd.log

sleep 1
# start gpsd
gpsd -P $demo_path/persist/$NODE_NO/var/run/gpsd.pid -G -n -b $(cat $demo_path/persist/$NODE_NO/var/run/gps.pty)

# start opentestpointd
# otestpointd -d $demo_path/otestpointd$NODE_NO.xml
otestpointd $demo_path/otestpointd$NODE_NO.xml -d -l 4 -f $demo_path/persist/$NODE_NO/var/log/otestpointd.log \
                    --pidfile $demo_path/persist/$NODE_NO/var/run/otestpointd.pid \
                    --uuidfile $demo_path/persist/$NODE_NO/var/run/otestpointd.uuid

# start opentestpoint recorder
otestpoint-recorder $demo_path/otestpoint-recorder$NODE_NO.xml -d -l 4 -f $demo_path/persist/$NODE_NO/var/log/otestpoint-recorder.log \
                    --pidfile $demo_path/persist/$NODE_NO/var/run/otestpoint-recorder.pid \
                    --uuidfile $demo_path/persist/$NODE_NO/var/run/otestpoint-recorder.uuid

#start mgen
starttime=
startoption=""
if [ -n "$starttime" ]; then
    startoption="start $(date --date "$starttime" "+%H:%M:%S" --utc)GMT"
fi

mgen input $demo_path/my-mgen \
     output $demo_path/persist/$NODE_NO/var/log/mgen.out  \
     $startoption
     txlog &> $demo_path/persist/$NODE_NO/var/log/mgen.log