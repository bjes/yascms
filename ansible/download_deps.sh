#!/bin/bash
rm -rf roles/*
ansible-galaxy role install -r requirements.yml
if [ -e collections/ansible_collections ]; then
    rm -rf collections/ansible_collections/*
fi
ansible-galaxy collection install -r requirements.yml
