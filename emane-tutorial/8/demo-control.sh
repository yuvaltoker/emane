DC_YML='/home/user2/work/idf/emane/dockercomposes/emane-net-demo8.yml'
HELPER_NAME='helper-service'

usage()
{
    echo 'Usage: ./demo-control.sh [OPTIONS]'
    echo
    echo 'A script for managing demo8'
    echo
    echo 'Options:'
    echo '    -c, --check  check tables on containers'
    echo '    -d, --down   gets demo down'
    echo '    -h, --help   print this usage and exit'
    echo '    -l, --log    print containers logs'
    echo '    -u, --up     gets demo up'
    echo
}

check()
{
    ../../check_on_containers.sh
}

down()
{
    docker-compose -f $DC_YML down -t 0
}

log()
{
    docker-compose -f $DC_YML logs
}

up()
{
    # get demo up + init each node via entrypoint
    docker-compose -f $DC_YML up -d --build
    # init helper
    docker exec -it $HELPER_NAME /bin/sh /emane-tutorial/8/init-helper.sh
}

# Loop through arguments and process them
for arg in "$@"
do
    case $arg in
        -c|--check)
        check
        exit 1
        ;;
        -d|--down)
        down
        exit 1
        ;;
        -h|--help)
        usage
        exit 1
        ;;
        -l|--log)
        log
        exit 1
        ;;
        -u|--up)
        up
        exit 1
    esac
done
