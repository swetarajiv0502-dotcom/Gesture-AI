# GestureVision (Gesture-AI)

Control your desktop with hand gestures. GestureVision watches your webcam, recognizes hand gestures in real time with MediaPipe, and maps each gesture to a system action — moving the cursor, clicking, controlling media/volume, switching slides, launching apps, or firing custom keyboard shortcuts. It ships as a small always-on-top Electron widget backed by a Python detection engine.

## Features

- **Real-time hand tracking** using MediaPipe's Hand Landmarker, streamed to the UI as a live annotated video feed
- **9 built-in gestures**: Open Palm, Closed Fist, Pointing Finger, Pinch, Victory Sign, Thumbs Up, Thumbs Down, Three Fingers, Rock Sign
- **Configurable action mapping** — reassign any gesture to a different action (or a custom keyboard shortcut) from the UI, persisted to a local SQLite database
- **Continuous cursor control** — point to move the mouse, using relative fingertip motion
- **Discrete actions with cooldown** — clicks, media controls, volume, app launching, window management, copy/paste/undo, and more
- **Action history log** stored in SQLite and viewable in the app
- **Compact always-on-top desktop widget** (Electron) that talks to the detection engine over WebSocket

## Architecture

```
┌─────────────────────┐        WebSocket (ws://localhost:8765)       ┌──────────────────────┐
│   Frontend (React)  │  <──────────────────────────────────────────>│  Backend (Python)     │
│   Electron widget    │                                              │  main.py               │
│   frontend/           │                                              │  ├─ webcam.py (capture)│
└─────────────────────┘                                              │  ├─ detector.py (MediaPipe hand landmarks)
                                                                        │  ├─ classifier.py (landmarks → gesture name)
                                                                        │  ├─ automation.py (gesture → OS action, pyautogui)
                                                                        │  └─ database.py (SQLite: mappings + history)
                                                                        └──────────────────────┘
```

The Python backend opens the webcam, detects hand landmarks each frame, classifies the landmarks into a named gesture, looks up the mapped action in SQLite, executes it, and broadcasts the annotated frame + gesture + action over a WebSocket to the React/Electron frontend.

## Tech Stack

**Backend:** Python, [MediaPipe](https://developers.google.com/mediapipe) (Hand Landmarker), OpenCV, `websockets`, `pyautogui`, SQLite

**Frontend:** React 19, Vite, Electron, Tailwind CSS, `lucide-react` icons

## Prerequisites

- Python 3.10+ and pip
- Node.js 18+ and npm
- A webcam
- Windows is currently the primary target (media keys, `start`/`explorer`/`calc` launchers, and `start.ps1` are Windows-specific); macOS/Linux users can still run the backend and frontend manually but should expect to adapt `automation.py`'s app-launching commands

## Setup

### 1. Backend (Python)

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install opencv-python mediapipe websockets pyautogui
```

The backend expects a `hand_landmarker.task` model file in the `backend/` directory (already included in this repo). It also uses a `gestures.db` SQLite file, which is created/reset automatically on startup with the default gesture-to-action mappings.

### 2. Frontend (React + Electron)

```bash
cd frontend
npm install
```

## Running the App

### Option A — One-command launch (Windows)

From the project root:

```powershell
.\start.ps1
```

This frees up ports `8765` (backend) and `5173` (Vite dev server), then runs `npm run electron:dev`, which starts Vite, waits for it to come up, and launches the Electron widget. Electron in turn spawns the Python backend from `backend/venv/Scripts/python.exe`, so make sure the virtual environment was created inside `backend/venv` (as in the setup step above).

### Option B — Manual / cross-platform

Run the backend and frontend in separate terminals:

```bash
# Terminal 1 — backend
cd backend
venv\Scripts\activate
python main.py
```

```bash
# Terminal 2 — frontend (browser)
cd frontend
npm run dev
```

Then open the printed Vite URL (typically `http://localhost:5173`) in your browser, or run `npm run electron:dev` to launch it as a desktop widget instead.

Click **Start Detection** in the UI to begin streaming webcam frames and recognizing gestures.

## Default Gesture Mappings

| Gesture | Default Action |
|---|---|
| Open Palm | No Action |
| Closed Fist | ⏯️ Play / Pause |
| Pointing Finger | 🖱️ Move Cursor |
| Pinch | 🖱️ Left Click |
| Victory Sign | ▶️ Next Slide |
| Thumbs Up | 🔊 Volume Up |
| Thumbs Down | 🔉 Volume Down |
| Three Fingers | 🌐 Open Chrome |
| Rock Sign | 🔇 Mute |

Every mapping can be changed from the app's Settings/Mappings view. Available actions include cursor move/click, media controls, volume, scrolling, alt-tab, close window, copy/paste/undo, opening Chrome/Explorer/Calculator/VS Code/Spotify/Terminal, and a custom keyboard shortcut (e.g. `ctrl+shift+esc`).

## Project Structure

```
Gesture-AI/
├── backend/
│   ├── main.py             # WebSocket server + detection loop
│   ├── webcam.py           # Webcam capture wrapper
│   ├── detector.py         # MediaPipe hand landmark detection + drawing
│   ├── classifier.py       # Landmark geometry → gesture name
│   ├── automation.py       # Gesture → OS action execution (pyautogui)
│   ├── database.py         # SQLite mappings + history
│   └── hand_landmarker.task
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main UI (live feed, mappings, history)
│   │   └── ...
│   ├── main.cjs            # Electron main process
│   └── package.json
└── start.ps1                # Windows one-command launcher
```

## Notes & Limitations

- Only the first detected hand is used for gesture classification per frame.
- Discrete actions (clicks, media keys, app launches, etc.) have a 1.2s cooldown to avoid repeat-firing; cursor movement is continuous and not subject to the cooldown.
- No `requirements.txt` is currently checked in — install the backend packages listed above manually, or generate one with `pip freeze > requirements.txt` after setup.

## License

No license file is currently included in this repository. Add one (e.g. MIT) if you intend for others to reuse this code.
