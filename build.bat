@echo off
@chcp 65001 1> NUL 2> NUL
setlocal

set script_dir=%~dp0
set HOME_DIR=%script_dir%

echo.
echo "[빌드] 도커 이미지 빌드를 시작합니다..."
echo.
docker build -f docker/Dockerfile -t he-lab .

if %errorlevel% equ 0 (
    echo.
    echo "[성공] 빌드가 완료되었습니다!"
    echo.
    echo "다음 명령어로 실행하세요"
    echo "   테스트 모드 = run_test.bat"
    echo "   PC A 서버 = run_server.bat"
    echo "   PC B 클라이언트 = run_client.bat"
    echo.
) else (
    echo.
    echo "[오류] 빌드에 실패했습니다. Docker Desktop이 실행 중인지 확인하세요."
    echo.
    exit /b 1
)
pause
