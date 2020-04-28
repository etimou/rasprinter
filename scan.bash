#!/bin/bash

# Set target file name.
file="Scan_$(date +%d-%m-%y)_$(date +%H-%M-%S)"

sudo scanimage -l 0 -t 0 -x 210 -y 297 --resolution 150 --mode Gray > /home/pi/scan.pnm


convert /home/pi/scan.pnm -level 25% /home/pi/final-%02d.pnm
convert /home/pi/final*.pnm -level 50%%,80%%,0.3 /home/pi/dark-%02d.pnm
convert /home/pi/dark*.pnm /home/pi/scan_f.pdf

gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen -sOutputFile=/home/pi/${file}.pdf /home/pi/scan_f.pdf




cp /home/pi/${file}.pdf /media/backup/data/scan/
rm /home/pi/*.pdf
rm /home/pi/*.pnm


