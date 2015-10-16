#!/usr/bin/env sh
#    author    :   丁雪峰
#    time      :   2015-05-12 17:17:27
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

pidfile="/tmp/hail.pid"
logfile="/tmp/uwsgi.log"

start(){
    ini=$(dirname $(realpath $0))/uwsgi.ini
    if [ ! -f $ini ]
    then
        echo 'not found uwsgi.ini ...'
        return
    fi
    cd $(dirname $(realpath $0))
    uwsgi --ini uwsgi.ini  --pidfile  $pidfile  --daemonize  $logfile
}

stop(){
    if [ ! -f $pidfile ]
    then
        echo 'no pidfile ...'
        return
    fi
    uwsgi --stop $pidfile
    echo 'stop ...'
}


case $1 in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        sleep 1
        start
        ;;
    status)
        echo ''
        ;;
    reload)
        uwsgi --reload $pidfile
        ;;
    log)
        tail -f  $logfile
        ;;
esac
