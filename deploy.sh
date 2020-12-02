#!/bin/bash
if [ $EUID -ne 0 ]; then
    echo "請使用 root 權限執行此 script"
    exit 1
fi

if [ "$1" != "project_only" ]; then
    apt install build-essential python3-dev python3-venv -y
fi
python3 -m venv .venv --system-site-packages
.venv/bin/pip install 'pip==20.2.4' 'wheel==0.36.0' 'setuptools==50.3.2' 'ansible==2.10.4' 'poetry==1.1.4'
.venv/bin/poetry run bash -c 'cd ansible && ./download_all_roles.sh'

if [ "$1" == "project_only" ]; then
    .venv/bin/poetry run ansible-playbook ansible/deploy.yml --extra-vars="@ansible/deploy.conf" --tags deploy_project_only
else
    .venv/bin/poetry run ansible-playbook ansible/deploy.yml --extra-vars="@ansible/deploy.conf"
fi
