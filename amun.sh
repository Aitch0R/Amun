#!/bin/bash
if [ $1 = update ]
then
	rm -rf temp
	git clone https://github.com/Aitch0R/Amun/ temp
	rm -r -f temp/.git
	rm -r Amun
	mv temp/* .
	rm -rf temp
fi
if [ $1 = start ]
then
	python3 -i Amun/amun.py
fi
