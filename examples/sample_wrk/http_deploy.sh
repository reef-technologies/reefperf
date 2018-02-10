#!/bin/bash -eu

user=$1
host=$2
port=$3
key_path=$4

ssh -o StrictHostKeyChecking=no -o LogLevel=ERROR -o UserKnownHostsFile=/dev/null "$user"@"$host" -p "$port" -i "$key_path" <<- 'EOF'
   python3 -m http.server &>/dev/null &
   exit
EOF

echo "<<<<<"
echo "http=http://$host:8000"
echo ">>>>>"
