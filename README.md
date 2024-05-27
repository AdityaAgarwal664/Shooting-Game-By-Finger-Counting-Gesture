# Finger Shooting Missile Game[An A<sup>2</sup> Product]

## Overview
Finger Shooting Missile is a gesture-based game where players use hand gestures detected by their webcam to shoot down missiles. The game leverages OpenCV for webcam input, MediaPipe for hand gesture recognition, and Pygame for the game mechanics and graphics.

## Features
- Hand gesture recognition using MediaPipe
- Real-time gameplay with webcam input
- Simple and intuitive controls: use your fingers to shoot down missiles
- Keeps track of score and highest score
- Sound effects for various actions in the game

## Requirements
- Python 3.7+
- Pygame 2.1.0
- MediaPipe 0.8.9
- OpenCV 4.5.5.64

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/AdityaAgarwal664/Shooting-Game-By-Finger-Counting-Gesture.git
   cd finger-shooting-missile
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play
1. Run the game script:
   ```bash
   python finger_shooting_missile.py
   ```
2. A window will open with the game's start menu. Click the "Play" button to start the game.
3. Use your fingers to shoot down the missiles:
   - Raise 1 finger to shoot missiles in Area 1
   - Raise 2 fingers to shoot missiles in Area 2
   - Raise 3 fingers to shoot missiles in Area 3
   - Raise 4 fingers to shoot missiles in Area 4
4. If a missile reaches the ground, the game is over. Click the "Replay" button to try again.
5. Try to achieve the highest score!

## Demo
[Link to Demo Video](https://youtu.be/XYPtFBfw4lU)

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments
- [MediaPipe](https://github.com/google/mediapipe) for the hand tracking solution
- [Pygame](https://www.pygame.org/news) for the game development library
- [OpenCV](https://opencv.org/) for the computer vision library


