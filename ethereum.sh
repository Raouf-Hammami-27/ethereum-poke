#!/usr/bin/env bash

apt-get install --yes --allow-unauthenticated wget

apt-get update && apt-get install --yes --allow-unauthenticated software-properties-common

add-apt-repository ppa:ethereum/ethereum

apt-get update && apt-get install --yes --allow-unauthenticated geth

adduser --disabled-login --gecos "" eth_user

mkdir /home/eth_user/eth_common

cp -r eth_common /home/eth_user/eth_common

wget -P /home/eth_user https://raw.githubusercontent.com/fishbullet/Ethereum-Private-Network/master/eth_common/genesis.json

chown -R eth_user:eth_user /home/eth_user/eth_common

su - eth_user

cd /home/eth_user

geth --rpc --mine --rpcaddr 172.10.0.10 --rpcport "8085" --rpcapi="db,eth,web3,personal,web3,miner" --datadir data --networkid 123 --nodiscover --maxpeers  0 init genesis.json