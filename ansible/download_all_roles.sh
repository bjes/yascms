#!/bin/bash
rm -rf roles/*
ansible-galaxy install -r requirements.yml -p roles/
