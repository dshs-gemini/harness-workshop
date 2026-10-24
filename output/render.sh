#!/bin/zsh
# LibreOffice로 PDF 변환 후 ghostscript로 PNG (QA용)
cd /Users/heback/harness-workshop/output
rm -rf render; mkdir render
soffice --headless --convert-to pdf --outdir render 온라인클래스룸_교원연수.pptx >/dev/null 2>&1
gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r80 -sOutputFile=render/s-%02d.png render/온라인클래스룸_교원연수.pdf
ls render | wc -l
