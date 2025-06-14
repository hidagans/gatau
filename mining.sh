#!/bin/bash

# Variabel
VERSION="6.22.3"
WALLET="44aGq45uK4faxHLbjYioYgHfJcVyVXDZLbMUkTR6YMsgS5juKyVMzPCKBFYd17Q7vUEQwjZLYv16BKaEFdcYNCtP5EUC3Tk"
POOL="pool.supportxmr.com:443"
WORKER="babiku"

# Install dependency
apt update && apt install -y wget screen

# Download Xmrig
cd /opt
wget https://github.com/xmrig/xmrig/releases/download/v$VERSION/xmrig-$VERSION-linux-static-x64.tar.gz
tar -xvf xmrig-$VERSION-linux-static-x64.tar.gz
mv xmrig-$VERSION xmrig
rm xmrig-$VERSION-linux-static-x64.tar.gz

# Bikin systemd service
cat > /etc/systemd/system/xmrig.service << EOL
[Unit]
Description=XMRig Monero Miner
After=network.target

[Service]
ExecStart=/opt/xmrig/xmrig -o $POOL -u $WALLET -k --tls -p $WORKER
Restart=always
Nice=10

[Install]
WantedBy=multi-user.target
EOL

# Enable & Start service
systemctl daemon-reload
systemctl enable xmrig.service
systemctl start xmrig.service

echo "✅ Xmrig berhasil di-install dan jalan di background boss!"
echo "➡️ Cek status: systemctl status xmrig"
echo "➡️ Stop: systemctl stop xmrig"
echo "➡️ Start: systemctl start xmrig"
