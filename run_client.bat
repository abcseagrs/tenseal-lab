@echo off
@chcp 65001 1> NUL 2> NUL
setlocal

echo.
echo "[PC B 클라이언트] 동형암호 클라이언트를 시작합니다"
echo.
echo "이 PC의 역할"
echo "   PC A로부터 공개 키 수신"
echo "   데이터 암호화"
echo "   암호화된 데이터를 PC A로 전송"
echo.
echo "========================================="
echo "IP 주소 입력 안내"
echo "========================================="
echo "같은 PC에서 테스트"
echo "   입력: host.docker.internal"
echo.
echo "다른 PC와 실습"
echo "   입력: PC A의 실제 IP 주소"
echo "   예: 192.168.0.10"
echo "========================================="
echo.
echo "클라이언트를 시작합니다..."
echo.

docker rm -f pc_b 2>nul
docker run -it --name pc_b he-lab bash -c "cd /app && python src/pc_b.py"
