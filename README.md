# Hand-Tracking Survival Game 🎮👋

A real-time computer vision game that combines OpenCV hand tracking with Pygame for an immersive survival experience. Control your character using hand gestures detected through your webcam while dodging obstacles and evading an intelligent chaser.

## 🎯 Game Overview

Players use their index finger to control a character on screen, navigating through increasingly challenging obstacles:
- **Random Shapes**: Colored geometric shapes spawn from screen edges with random velocities
- **Smart Chaser**: An AI-controlled circle that actively pursues the player, growing larger and faster over time
- **Progressive Difficulty**: Game becomes more challenging as survival time increases

## 🕹️ Controls

- **Movement**: Point your index finger at the camera - your character follows your finger position
- **Objective**: Survive as long as possible by avoiding all obstacles and the chaser

## 🎨 Visual Features

- **Dynamic Chaser**: Changes color based on difficulty level (Green → Blue → Red)
- **Multiple Shape Types**: Rectangles, circles, and triangles with different spawn patterns
- **Real-time Stats**: Survival time display and performance metrics

## 🛠️ Technology Stack

- **OpenCV**: Real-time computer vision and hand detection
- **MediaPipe**: Advanced hand landmark detection
- **Pygame**: Game engine and graphics rendering
- **Python**: Core programming language

## 📋 Requirements

```bash
pip install opencv-python
pip install mediapipe
pip install pygame
```

## 🚀 How to Run

1. Clone the repository
2. Install required dependencies
3. Ensure your webcam is connected and functional
4. Run the game: `python main.py`
5. Position your hand in front of the camera and start playing!

## 🎮 Game Mechanics

- **Collision Detection**: Advanced collision algorithms for precise hit detection
- **Adaptive AI**: Chaser speed and size increase with survival time
- **Edge Spawning**: Obstacles appear from screen borders with realistic physics
- **Performance Optimization**: Efficient shape management and rendering

## 🏆 Challenge Yourself

Try to survive as long as possible! The game tracks your survival time and becomes progressively more difficult, testing your reflexes and hand-eye coordination.
