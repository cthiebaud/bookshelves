ffmpeg -i input_video.mov -c:v libx264 -crf 23 -c:a aac -strict experimental -b:a 128k output_video.mp4
