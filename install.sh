#!/bin/bash

# === Renkler ===
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Web Site Cloner Setup Started...${NC}"

# === Python Kontrolü ===
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}[❌] Python3 bulunamadı! Kuruluyor...${NC}"
    sudo apt update && sudo apt install -y python3
else
    echo -e "${GREEN}[✅] Python3 yüklü.${NC}"
fi

# === Pip Kontrolü ===
if ! command -v pip3 &>/dev/null; then
    echo -e "${RED}[❌] Pip3 bulunamadı! Kuruluyor...${NC}"
    sudo apt install -y python3-pip
else
    echo -e "${GREEN}[✅] Pip3 yüklü.${NC}"
fi

# === Virtualenv Kontrolü ===
if ! python3 -m venv --help &>/dev/null; then
    echo -e "${RED}[❌] Virtualenv modülü bulunamadı! Kuruluyor...${NC}"
    sudo apt install -y python3-venv
else
    echo -e "${GREEN}[✅] Virtualenv kullanılabilir.${NC}"
fi

# === Sanal Ortam Kurulumu ===
if [ ! -d "venv" ]; then
    echo -e "${GREEN}[+] Sanal ortam oluşturuluyor...${NC}"
    python3 -m venv venv
fi

# === Sanal Ortamı Etkinleştir ===
echo -e "${GREEN}[+] Sanal ortam aktifleştiriliyor...${NC}"
source venv/bin/activate

# === Gerekli Paketleri Yükle ===
echo -e "${GREEN}[+] Gerekli Python kütüphaneleri yükleniyor...${NC}"
pip install --upgrade pip
pip install requests beautifulsoup4

# === Çalışma Dizini Kontrolü ===
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# === Dosya Kontrolü ===
if [ ! -f "clone-website.py" ]; then
    echo -e "${RED}[❌] clone-website.py bulunamadı! Lütfen aynı dizinde olduğuna emin olun.${NC}"
    exit 1
fi

# === Scripti Çalıştır ===
echo -e "${GREEN}✅ Kurulum tamamlandı! Script başlatılıyor...${NC}"
python3 clone-website.py
