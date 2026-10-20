#!/usr/bin/env bash
# Kabine sosyal medya çalışma ortamını hazırlar: yazı tipleri, Instagram araç seti, Python paketleri.
# Oyunun HTML'i (game/kabine.html) burada indirilmez: Claude oturumunda Artifact `read` ile alınıp kopyalanır (bkz. CLAUDE.md).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "== Python paketleri"
python3 -c "import playwright, cv2, numpy, scipy, PIL" 2>/dev/null || pip install --break-system-packages -q playwright opencv-python-headless numpy scipy pillow
command -v ffmpeg >/dev/null || { echo "ffmpeg yok: apt-get install -y ffmpeg"; exit 1; }

echo "== Yazı tipleri (Google Fonts deposundan, sadece gereken aileler)"
if [ ! -d fonts/gf/ofl/anton ]; then
  mkdir -p fonts && cd fonts
  [ -d gf ] || git clone --depth 1 --filter=blob:none --sparse https://github.com/google/fonts.git gf
  cd gf && git sparse-checkout set --no-cone /ofl/pixelifysans/ /ofl/barlowsemicondensed/ /ofl/oldstandardtt/ /ofl/anton/ /ofl/bungee/
  cd "$ROOT"
fi

echo "== Instagram araç seti (MIT)"
[ -d igkit ] || git clone --depth 1 https://github.com/Jakeschincariol/instagram-agent-skill.git igkit

echo "== Oyun dosyası"
if [ -f game/kabine.html ]; then echo "game/kabine.html hazır"; else echo "EKSİK: game/kabine.html (Artifact WdwvebzHNYc8eboHZivxNi'yi oku ve buraya kopyala)"; fi
echo "Tamam."
