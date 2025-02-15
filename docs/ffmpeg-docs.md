# FFmpeg Docs

---

## **Best ffmpeg frame pre-processing commands**

```
ffmpeg -i fort4.mp4 -vf "fps=2,format=bgr24,colorchannelmixer=.19:.19:.19:0:.19:.19:.19:0:.19:.19:.19:0,eq=saturation=0.0:contrast=7.0:brightness=0.5,format=yuv420p" frames/frame_%04d.png
```
```
ffmpeg -i fort4.mp4 -vf "fps=2,format=bgr24,colorchannelmixer=.18:.18:.18:0:.18:.18:.18:0:.18:.18:.18:0,eq=saturation=0.0:contrast=8.0:brightness=0.7,format=yuv420p" frames/frame_%04d.png
```
```
ffmpeg -i fort4.mp4 -vf "fps=2,format=bgr24,colorchannelmixer=.23:.23:.23:0:.23:.23:.23:0:.23:.23:.23:0,eq=saturation=0.0:contrast=6.0:brightness=0.0,format=yuv420p" frames/frame_%04d.png
```
```
ffmpeg -i fort4.mp4 -vf "fps=2,format=bgr24,colorchannelmixer=.21:.21:.21:0:.21:.21:.21:0:.21:.21:.21:0,eq=saturation=0.0:contrast=6.0:brightness=0.2,format=yuv420p" frames/frame_%04d.png
```
```
ffmpeg -i fort4.mp4 -vf "fps=2,format=bgr24,colorchannelmixer=.18:.18:.18:0:.18:.18:.18:0:.18:.18:.18:0,eq=saturation=0.0:contrast=7.0:brightness=0.6,format=yuv420p" frames/frame_%04d.png
```
```
ffmpeg -i fort4.mp4 -vf "fps=2,format=bgr24,colorchannelmixer=.16:.16:.16:0:.16:.16:.16:0:.16:.16:.16:0,eq=saturation=0.0:contrast=8.0:brightness=1.0,format=yuv420p" frames/frame_%04d.png
```
```
ffmpeg -i fort4.mp4 -vf "fps=2,format=bgr24,colorchannelmixer=.21:.21:.21:0:.21:.21:.21:0:.21:.21:.21:0,eq=saturation=0.0:contrast=7.0:brightness=0.2,format=yuv420p" frames/frame_%04d.png
```
```
ffmpeg -i fort4.mp4 -vf "fps=2,format=bgr24,colorchannelmixer=.17:.17:.17:0:.17:.17:.17:0:.17:.17:.17:0,eq=saturation=0.0:contrast=7.0:brightness=0.7,format=yuv420p" frames/frame_%04d.png
```
