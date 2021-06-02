DC_YML='/home/user2/work/idf/emane/dockercomposes/emane-net-demo8.yml'
HELPER_NAME='helper-service'

usage()
{
    echo 'Usage: ./build-script.h [OPTIONS]'
    echo
    echo 'A script for managing demo8'
    echo
    echo 'Options:'
    echo '    -d, --down  gets demo down'
    echo '    -h, --help  Print this usage and exit'
    echo '    -u, --up    gets demo up'
    echo
}

down()
{
    docker-compose -f $DC_YML down -t 0
}

up()
{
    # get demo up + init each node via entrypoint
    docker-compose -f $DC_YML up -d
    # init helper
    docker exec -it $HELPER_NAME /bin/sh /emane-tutorial/8/init-helper.sh
}

# Loop through arguments and process them
for arg in "$@"
do
    case $arg in
        -d|--down)
        down
        exit 1
        ;;
        -h|--help)
        usage
        exit 1
        ;;
        -u|--up)
        up
        exit 1
    esac
done