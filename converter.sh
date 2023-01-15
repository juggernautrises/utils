#!/bin/zsh
src_files=($1/*.flac)
for file in $src_files
do
  file=${file%.*}
  input="$file.flac"
  output="$file.mp3"
   ffmpeg -y -i $input -ab 320k -map_metadata 0 -id3v2_version 3 $output
done
