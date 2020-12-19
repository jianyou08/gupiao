#!/bin/bash

app="python3 web_web.py 80"
logfile=".logs/web.log"

run_mode="$2"

function getpid()
{
    pid=`ps -ef | grep "$app" | grep -v grep | awk '{print $2}'`
    echo "$pid"
    return
}

function stop()
{
    pid=`getpid`
    if [ "x$pid" == "x" ]; then
        echo "$app is not running"
    else
        echo " stop..."
        kill -9 $pid
    fi
}

function start()
{
    pid=`getpid`
    if [ "x$pid" == "x" ]; then
        echo " start..."
        if [ "x$run_mode" == "xdebug" ]; then
            $app &
        else
            nohup $app > $logfile 2>&1 &
        fi
    else
        echo "$app is running: %pid"
    fi
}

function check()
{
    pid=`getpid`
    if [ "x$pid" == "x" ]; then
        echo "$app not running!!!"
        start
    else
        echo "$app is running:$pid"
    fi
}

case "x$1" in
    "xstop")
        stop
        ;;

    "xstart")
        start
        ;;

    "xrestart")
        stop
        start
        ;;

    "xcheck")
        check
        ;;

    *)
        check
        ;;
esac

