container_no=""
emanesh_command="get table nems mac RxSlotStatusTable"



if [ "$container_no" = "" ]; then 
    for i in $(seq 1 10); do docker exec -it emane-service$i emanesh localhost $emanesh_command; done
else
    docker exec -it emane-service$container_no emanesh localhost $emanesh_command
fi