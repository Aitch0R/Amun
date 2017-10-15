#!/bin/bash
if [ $1 = update ]
then
	git pull original master
fi
if [ $1 = start ]
then
	python3 -i Amun/amun.py
fi
