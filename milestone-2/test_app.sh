#!/bin/bash -eu

wget "http://$1:$2/"
cat index.html
