#!/bin/bash
if [ $EUID -ne 0 ]; then
    echo "請使用 root 權限執行此 script"
    exit 1
fi
apt update
apt install build-essential python3-dev python3-venv python3-pip -y
pip3 install pip setuptools ansible --user --upgrade
export PATH=~/.local/bin:$PATH
cd ansible && ./download_all_roles.sh && cd -
~/.local/bin/ansible-playbook ansible/deploy.yml --extra-vars="@ansible/deploy.conf"
