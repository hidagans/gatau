#!/bin/bash

# Nama file: pkt_install.sh

echo "Installing PKT Miner..."

# Install dependencies
sudo apt install gcc git make curl libc6-dev -y

# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Source cargo environment
source $HOME/.cargo/env

# Install PacketCrypt
~/.cargo/bin/cargo install --git https://github.com/pkt-world/packetcrypt_rs.git --locked --features jit

# Start mining
~/.cargo/bin/packetcrypt ann -p pkt1qt5qkf4mx9jzwfa8gl6sylvcy5sxvzzsyyqrguf http://pool.pkt.world
