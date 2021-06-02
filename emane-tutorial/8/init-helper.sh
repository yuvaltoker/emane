cd /emane-tutorial/8
emaneeventservice -d eventservice.xml -l 3 -f persist/helper/var/log/emaneeventservice.log \
                                    --pidfile persist/helper/var/run/emaneeventservice.pid \
                                    --uuidfile persist/helper/var/run/emaneeventservice.uuid
emaneevent-tdmaschedule schedule.xml -i emane0