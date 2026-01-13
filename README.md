# plymouth-animation

generates limeos boot splash animation for plymouth

## run

```
uv run main.py
```

needs ffmpeg installed

## output

generates `output-light/` and `output-dark/` folders with:
- frame-*.png (animation frames)
- preview.mp4 (preview vid)
- limeos.plymouth + limeos.script (theme files)

## preview

light theme:

https://github.com/user-attachments/assets/placeholder-light

dark theme:

https://github.com/user-attachments/assets/placeholder-dark

(after running, drag the preview.mp4 files into a github issue/pr to get embed urls, then replace the placeholders above)

## config

edit the top of main.py if u wanna change stuff
