#!/bin/zsh
set -euo pipefail

cd "$(dirname "$0")"

port=18771
iface="$(route -n get default 2>/dev/null | awk '/interface:/{print $2; exit}')"
ip=""
if [[ -n "$iface" ]]; then
  ip="$(ipconfig getifaddr "$iface" 2>/dev/null || true)"
fi

echo "本地服务目录：$(pwd)"
if [[ -n "$ip" ]]; then
  echo "iPhone 与 Mac 需在同一局域网。"
  echo "插件 URL：http://$ip:$port/Douban.lpx"
else
  echo "未检测到局域网 IPv4 地址，请检查 Wi-Fi。"
fi
echo "关闭此窗口或按 Ctrl+C 即停止服务。"
echo

python3 -m http.server "$port" --bind 0.0.0.0
