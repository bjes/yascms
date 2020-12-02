#!/bin/bash
if [ $EUID -ne 0 ]; then
    echo "請使用 root 權限執行此 script"
    exit 1
fi

if [ "$1" != "project_only" ]; then
    apt install build-essential python3-dev python3-venv -y
fi
python3 -m venv .venv
.venv/bin/pip install 'pip==20.3' 'setuptools==50.3.2' 'ansible==2.10.4' 'poetry==1.1.4'
.venv/bin/poetry run bash -c 'cd ansible && ./download_all_roles.sh'
.venv/bin/poetry run ansible-playbook ansible/deploy.yml --extra-vars="@ansible/deploy.conf"
