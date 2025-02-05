#!/bin/bash

# Update dan instal dependensi yang diperlukan
echo "Memulai instalasi..."
sudo apt update
sudo apt install -y wget screen tar

# Unduh file miner
echo "Mengunduh SRBMiner..."
wget https://github.com/doktor83/SRBMiner-Multi/releases/download/2.4.6/SRBMiner-Multi-2-4-6-Linux.tar.xz

# Ekstrak file
echo "Ekstraksi file..."
tar -xvf SRBMiner-Multi-2-4-6-Linux.tar.xz

# Masuk ke direktori miner
cd SRBMiner-Multi-2-4-6

# Mendapatkan jumlah core CPU yang tersedia
CPU_THREADS=$(nproc)

# Membuat screen baru dan menjalankan miner dengan jumlah thread sesuai CPU
echo "Menjalankan miner di dalam screen dengan $CPU_THREADS threads..."
screen -dmS miner ./SRBMiner-MULTI --disable-gpu --algorithm verushash --pool ap.luckpool.net:3956 --wallet RJL4cPV7wxfigkdUWEFUdaMKgAiK8KoL2U --Worker VerusPC --password Hybrid --cpu-threads $CPU_THREADS

# Selesai
echo "Instalasi selesai. Anda dapat mengakses screen dengan perintah 'screen -r miner'."
