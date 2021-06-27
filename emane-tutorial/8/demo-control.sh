#DC_YML='/home/user2/work/idf/emane/dockercomposes/emane-net-demo8.yml'
DC_YML='/home/user2/work/idf/emane/dockercomposes/emane-net-probe-testing.yml'
HELPER_NAME='helper-service'
BUILD=''
is_check='F'
is_down='F'
is_help='F'
is_log='F'
is_up='F'

usage()
{
    echo 'Usage: ./demo-control.sh [OPTIONS]'
    echo
    echo 'A script for managing demo8'
    echo
    echo 'Options:'
    echo '    -b, --build  docker compose up will be called with build flag'
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
    docker-compose -f $DC_YML up -d $BUILD
    # init helper
    #docker exec -it $HELPER_NAME /bin/sh /emane-tutorial/8/init-helper.sh
}

# Loop through arguments and sign them
for arg in "$@"
do
    case $arg in
        -b|--build)
        is_build='T'
        ;;
        -c|--check)
        is_check='T'
        ;;
        -d|--down)
        is_down='T'
        ;;
        -h|--help)
        is_help='T'
        ;;
        -l|--log)
        is_log='T'
        ;;
        -u|--up)
        is_up='T'
    esac
done

# proccesss the variables with proccess logic
if [ "$is_help" = "T" ]; then
    usage
    exit 1
fi

if [ "$is_build" = "T" ]; then
    BUILD='--build'
fi

if [ "$is_up" = "T" ]; then
    up
    exit 1
fi

if [ "$is_down" = "T" ]; then
    down
    exit 1
fi

if [ "$is_check" = "T" ]; then
    check
    exit 1
fi

if [ "$is_log" = "T" ]; then
    log
    exit 1
fi

