#!/bin/bash
export app_dir=/opt/app
git clone $github_url /opt/app
if [ -f /opt/app/package.json ]
  cd  /opt/app/ && npm install
fi

cat > /etc/init/nodeapp.conf <<EOS
description "node.js app"

start on (net-device-up
and local-filesystems
and runlevel [2345])
stop on runlevel [!2345]

expect fork
respawn

script
export HOME=/
export NODE_PATH=/usr/lib/node
exec /usr/bin/node ${app_dir}/server.js >> /var/log/nodeapp.log 2>&1 &
end script
EOS
