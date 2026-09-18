@echo off
cd /d "%~dp0"
set PORT=%1
if "%PORT%"=="" set PORT=3000

if exist ".env" (
  for /f "usebackq eol=# tokens=1,* delims==" %%A in (".env") do (
    if not "%%A"=="" set "%%A=%%B"
  )
)

if "%DEEPSEEK_API_KEY%"=="" (
  echo Khong co DEEPSEEK_API_KEY: server van chay va UI se dung fallback co gan nhan.
)

echo VLearn Ready: http://localhost:%PORT%
echo Health check: http://localhost:%PORT%/api/health
python server.py --port %PORT%
pause
