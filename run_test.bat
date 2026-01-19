@echo off
@chcp 65001 1> NUL 2> NUL
setlocal

echo.
echo [테스트 모드] 단일 컨테이너에서 테스트를 실행합니다
echo.
echo "실행 방법"
echo "   1. 이 터미널에서 PC A (서버)가 실행됩니다"
echo "   2. 새 터미널을 열고 다음과 같이 실행하세요"
echo "      docker exec -it he-lab-test bash"
echo "      python src/pc_b.py"
echo "   3. IP 주소 입력 프롬프트에서 localhost 입력"
echo.
echo "PC A 서버를 시작합니다..."
echo.

docker rm -f he-lab-test 2>nul
docker run -it --name he-lab-test he-lab bash -c "cd /app && python src/pc_a.py"
