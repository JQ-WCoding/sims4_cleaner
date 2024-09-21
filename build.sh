#!/bin/bash

# PyInstaller 명령어를 실행하여 실행 파일을 생성합니다.
pyinstaller --onefile --windowed --icon=sims4_cleaner_imgae.ico cleaning.py

echo "빌드가 완료되었습니다. 'dist' 폴더를 확인하세요."