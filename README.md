<div align="center">
  <h1>🏓 KiPong</h1>
  <p>A classic, retro-styled 2-player Pong game built with Python and Kivy.</p>
</div>
🎮 About The Project
KiPong is a local multiplayer desktop game recreating the arcade experience of Pong. Built using the Kivy cross-platform UI framework, it features smooth 60 FPS mechanics, custom retro aesthetics including a Minecraft-style font, dynamic win/loss visual states, and sound effects.
The match continues until one player reaches a score threshold of 5 points, triggering a victory overlay and sound effect.
✨ Key Features
Local 2-Player Combat: Compete head-to-head on the same keyboard.
Fluid Physics & Gameplay: Custom paddle velocities, capped ball speeds, and collision multipliers for engaging gameplay.
Immersive UI/UX: Features a looping video background on the start screen and custom pixel-art interface buttons.
Audio Feedback: Authentic bouncing and victory sound effects powered by Kivy's `SoundLoader`.
Dynamic Game States: Color-coded overlays indicating WIN/LOST status with Kivy `Animation`.
🚀 Getting Started
Prerequisites
Make sure you have Python installed (preferably Python 3.12+).
Installation
Clone the repository:
```bash
   git clone https://github.com/yourusername/KiPong.git
   cd KiPong
   ```
Create a virtual environment (Recommended):
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
Install dependencies:
```bash
   pip install -r requirements.txt
   ```
🕹️ How to Play
Run the main game script from the `src` directory:
```bash
cd src
python main.py
```
Controls
Action	Player 1 (Left)	Player 2 (Right)
Move Up	`W`	`I`
Move Down	`S`	`J`
📁 Project Structure
```text
KiPong/
├── design/
│   ├── game_screen.kv
│   ├── loading_screen.kv
│   └── style.kv
├── resources/
│   ├── audio/        # Bounce and victory sounds
│   ├── buttons/      # Custom UI sprites
│   ├── fonts/        # Minecraft.ttf
│   └── video/        # PongBg.mp4
├── src/
│   ├── main.py
│   └── screens/
│       └── game_screen.py
└── requirements.txt
```
🛠️ Built With
Python
Kivy 2.3.1