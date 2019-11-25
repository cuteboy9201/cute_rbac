#!/bin/bash 
### 
# @Author: Youshumin
# @Date: 2019-11-15 12:01:01
 # @LastEditors: Please set LastEditors
 # @LastEditTime: 2019-11-25 16:22:06
# @Description: 
###

workdir=$(cd $(dirname $0); pwd) 
export PYTHONPATH=$PYTHONPATH:${workdir} 

pyenv="/data/code/rbac/.env/bin/python3.7"

start_main(){
    cd $workdir
    ${pyenv} run_server.py
}

rbac_db_init(){
    cd ${workdir}/data/db_init
    ${pyenv} module.py create
}

rbac_db_del(){
    cd ${workdir}/data/db_init
    ${pyenv} module.py drop 
}
case "$1" in 
    start)
        start_main
        ;;
    dbinit)
        rbac_db_init
        ;;
    *)
        echo "start, dbinit"
        ;;
esac