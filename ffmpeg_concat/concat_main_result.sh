#!/bin/sh

quality=$1
if [ -z "$quality" ]; then
  quality="1440p60"
fi

rm /tmp/concat.txt
for f in media/videos/main_result/"$quality"/Scene*.mp4; do
  base="${f%.*}"
  ffmpeg -hide_banner -loglevel error -nostats -i "${base}.mp4" -i "${base}.srt" -sub_charenc utf8 -map 0:v -map 1 -t 60 -c:v copy -c:s copy -y "/tmp/$(basename $base).mkv"
  echo "file /tmp/$(basename $base).mkv" >> /tmp/concat.txt
done
ffmpeg -hide_banner -loglevel error -nostats -f concat -safe 0 -i /tmp/concat.txt -map 0:v -map 0:s -c:v libx264 -crf 22 -c:s copy -y media/videos/main_result/"$quality"/main_result.mkv
