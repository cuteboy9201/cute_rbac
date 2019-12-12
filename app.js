/*
 * @Author: your name
 * @Date: 2019-12-12 14:14:12
 * @LastEditTime: 2019-12-12 14:14:22
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: /rbac/app.js
 */
{
  "apps": [{
    "name": "cuteeyes-rbac",
    "script": "/data/code/rbac/.env/bin/python run_server.py",
    "cwd": "/data/code/rbac",
    "max_memory_restart": "100M",
    "log_file"   : "/data/logs/supervisord/cuteeyes-rbac.log",
    "error_file": "/dev/null",
    "out_file": "/dev/null",
    "pid_file": "/data/logs/supervisord/cuteeyes-rbac.pid",
    "autorestart": true,
    "node_args": [],
    "args": [],
    "env": { "RUN_ENV": "prod"
    }
  }]
}