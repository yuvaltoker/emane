container_no="2"
emanesh_command="set config "$container_no" mac delay=.92"



if [ "$container_no" = "" ]; then 
    for i in $(seq 1 10); do docker exec -it emane-service$i emanesh localhost $emanesh_command; done
else
    docker exec -it emane-service$container_no emanesh localhost $emanesh_command
fi