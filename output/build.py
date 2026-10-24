#!/usr/bin/env python3
"""연수 PPT 조립: 원고 파싱(notes.json) -> pptxgenjs 빌드(build.js) -> 검증.
사용: python3 build.py   (output/ 에서 npm install pptxgenjs 필요)"""
import subprocess, os
here = os.path.dirname(os.path.abspath(__file__))
subprocess.run(['python3', os.path.join(here, 'parse_notes.py')], check=True, cwd=here)
subprocess.run(['node', os.path.join(here, 'build.js')], check=True, cwd=here)
