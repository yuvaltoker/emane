
demo_path="/emane-tutorial/8"
cd $demo_path

rm -r $demo_path/persist/helper/var
mkdir -p $demo_path/persist/helper/var/log
mkdir -p $demo_path/persist/helper/var/run

emaneeventservice -d eventservice.xml -l 3 -f persist/helper/var/log/emaneeventservice.log \
                                    --pidfile persist/helper/var/run/emaneeventservice.pid \
                                    --uuidfile persist/helper/var/run/emaneeventservice.uuid
emaneevent-tdmaschedule schedule.xml -i eth0