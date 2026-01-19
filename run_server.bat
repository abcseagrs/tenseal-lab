@echo off
@chcp 65001 1> NUL 2> NUL
setlocal

echo.
echo "[PC A 서버] 동형암호 서버를 시작합니다"
echo.
echo "이 PC의 역할"
echo "   암호화 키 생성"
echo "   5000번 포트 대기"
echo "   데이터 복호화 및 결과 출력"
echo.
echo "중요! 자신의 IP 주소를 PC B에게 알려주세요"
echo "같은 PC 테스트: localhost 사용"
echo "다른 PC 실습: ipconfig로 IP 확인"
echo.
echo "서버를 시작합니다..."
echo.

docker rm -f pc_a 2>nul
docker run -it -p 5000:5000 --name pc_a he-lab bash -c "cd /app && python src/pc_a.py"
