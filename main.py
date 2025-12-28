import cv2, os, time, sys, shutil
from enum import Enum

class PlayMode(Enum):
    VIDEO = 1

# Important so the ascii can fit the screen
def terminal_size():
    return shutil.get_terminal_size()

# This is basically what turns the video into ASCII
def to_ascii(frame, chars, w, h):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (w, h))
    scale = (len(chars) - 1) / 255

    return "\n".join("".join(chars[int(px * scale)] for px in row) 
    for row in gray
    )

def play_in_terminal(video_path_or_cam_idx, black2white_chars, height, width, mode, max_fps):
    
    cap = cv2.VideoCapture(video_path_or_cam_idx) # <- Opens the video
    delay = 1 / max_fps

    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            ascii_frame = to_ascii(frame, black2white_chars, width, height - 1)

            sys.stdout.write("\033[H") 
            sys.stdout.write(ascii_frame)
            sys.stdout.flush()

            time.sleep(delay)
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        sys.stdout.write("\033[?25h\n")
        sys.stdout.flush()

# The main execution
if __name__ == "__main__":
    h, w = terminal_size().lines, terminal_size().columns
    print(f"Terminal size (h, w): ({h}, {w})")
    time.sleep(1)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(BASE_DIR, "video", "lain_dance.mp4") # Add any video you want. Just change lain_dance.mp4 to the video you got

    
    play_in_terminal(
        video_path_or_cam_idx = video_path,
        black2white_chars = [' ', '`', '.', '~', '+', '*', 'o', 'O', '0', '#', '@'],
        height = h,
        width = w,
        mode = PlayMode.VIDEO,
        max_fps = 60
    )