# AI Virtual Mouse 🖱️✋

A computer vision-based virtual mouse application that allows you to control your computer's cursor and perform mouse operations using hand gestures through your webcam.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.8+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- **Cursor Movement**: Move your cursor by pointing with your index finger
- **Left Click**: Bring index and middle fingers close together
- **Right Click**: Bring thumb and index finger close together
- **Drag & Drop**: Pinch with thumb and index finger, then move to drag
- **Real-time Hand Tracking**: Uses MediaPipe for accurate hand landmark detection
- **Smooth Movement**: Implements position smoothing and gesture stabilization
- **Customizable UI**: Toggle window properties and visual feedback
- **Cross-platform**: Works on Windows, macOS, and Linux

## 🎯 Hand Gestures

| Gesture                                                                              | Action          | Description                             |
| ------------------------------------------------------------------------------------ | --------------- | --------------------------------------- |
| ![Index Up](https://img.shields.io/badge/-Index%20Finger%20Up-blue)                  | **Move Cursor** | Point with index finger to move cursor  |
| ![Two Fingers Close](https://img.shields.io/badge/-Index%20+%20Middle%20Close-green) | **Left Click**  | Bring index and middle fingers together |
| ![Thumb Index Close](https://img.shields.io/badge/-Thumb%20+%20Index%20Close-orange) | **Right Click** | Pinch thumb and index finger            |
| ![Pinch and Move](https://img.shields.io/badge/-Pinch%20+%20Move-red)                | **Drag**        | Maintain pinch gesture while moving     |

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- Webcam
- Windows/macOS/Linux

### Install Dependencies

1. Clone this repository:

```bash
git clone https://github.com/yourusername/virtual-mouse.git
cd virtual-mouse
```

2. Install required packages:

```bash
pip install opencv-python mediapipe pyautogui numpy
```

Or install from requirements file:

```bash
pip install -r requirements.txt
```

### Alternative Installation Methods

**Using conda:**

```bash
conda install opencv mediapipe pyautogui numpy
```

**Using poetry:**

```bash
poetry install
```

## 🎮 Usage

### Running the Application

1. **From Jupyter Notebook:**

   - Open `virtual-mouse.ipynb` in Jupyter Lab/Notebook
   - Run all cells
   - The application will start automatically

2. **From Python Script:**
   ```bash
   python virtual_mouse.py
   ```

### Controls

#### Mouse Gestures

- **Move**: Point with index finger within the control area (purple rectangle)
- **Left Click**: Bring index and middle fingers close together
- **Right Click**: Pinch thumb and index finger
- **Drag**: Maintain pinch gesture while moving your hand

#### Keyboard Controls

| Key | Action                           |
| --- | -------------------------------- |
| `T` | Toggle always-on-top window      |
| `S` | Toggle small/large window size   |
| `L` | Toggle hand landmarks visibility |
| `Q` | Quit application                 |

### Tips for Best Performance

1. **Lighting**: Ensure good lighting conditions for better hand detection
2. **Background**: Use a contrasting background for improved tracking
3. **Distance**: Keep your hand 1-3 feet from the camera
4. **Stability**: Hold gestures for a moment to ensure detection
5. **Control Area**: Keep hand movements within the purple rectangle

## ⚙️ Configuration

### Adjustable Parameters

The application includes several configurable parameters in the `VirtualMouse` class:

```python
# Movement and gesture sensitivity
self.movement_threshold = 5      # Cursor movement sensitivity
self.click_distance = 40         # Distance for click detection
self.drag_distance = 35          # Distance for drag detection
self.smoothening = 5             # Movement smoothing factor

# Gesture stability
self.gesture_threshold = 3       # Frames to confirm gesture
self.click_cooldown = 0.3        # Cooldown between clicks

# Camera settings
self.frame_reduction = 100       # Control area margin
```

### Window Customization

- **Always on Top**: Keep the camera feed window above other applications
- **Size Toggle**: Switch between small (400x300) and large (640x480) window
- **Position**: Automatically positions window based on size setting

## 🏗️ Project Structure

```
virtual-mouse/
│
├── virtual-mouse.ipynb      # Main Jupyter notebook
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── assets/                 # Screenshots and demos (optional)
```

## 🔧 Technical Details

### Dependencies

- **OpenCV (cv2)**: Computer vision and camera handling
- **MediaPipe**: Hand landmark detection and tracking
- **PyAutoGUI**: System cursor control and mouse operations
- **NumPy**: Numerical computations and array operations

### Key Components

1. **HandDetector Class**: Wraps MediaPipe functionality for hand detection
2. **VirtualMouse Class**: Main application logic and gesture recognition
3. **Gesture Detection**: Frame-based gesture stabilization system
4. **Movement Smoothing**: Position history and interpolation for smooth cursor movement

### Algorithm Overview

1. **Capture**: Get video frame from webcam
2. **Detection**: Use MediaPipe to detect hand landmarks
3. **Analysis**: Calculate finger positions and distances
4. **Recognition**: Determine gesture based on finger states
5. **Stabilization**: Confirm gesture over multiple frames
6. **Execution**: Perform corresponding mouse action

## 🐛 Troubleshooting

### Common Issues

1. **Camera not detected:**

   - Check if camera is connected and working
   - Try changing camera index in `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)`

2. **Poor gesture recognition:**

   - Improve lighting conditions
   - Ensure hand is within the purple control area
   - Adjust detection confidence parameters

3. **Cursor movement too sensitive/slow:**

   - Modify `movement_threshold` and `smoothening` parameters
   - Adjust `frame_reduction` for larger control area

4. **PyAutoGUI permission issues (macOS):**
   - Grant accessibility permissions to Terminal/Python in System Preferences

### Performance Optimization

- Close unnecessary applications to free up CPU
- Reduce camera resolution if experiencing lag
- Adjust `gesture_threshold` for faster/more stable recognition

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:

1. **Bug Reports**: Submit issues with detailed descriptions
2. **Feature Requests**: Suggest new gestures or functionality
3. **Code Improvements**: Submit pull requests for enhancements
4. **Documentation**: Help improve documentation and examples

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with a clear description

## 📋 Future Enhancements

- [ ] Multi-hand support for advanced gestures
- [ ] Gesture customization interface
- [ ] Voice commands integration
- [ ] Mobile app companion
- [ ] Machine learning model training for custom gestures
- [ ] Support for multiple monitors
- [ ] Gesture macros and shortcuts

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **MediaPipe Team**: For the excellent hand tracking framework
- **OpenCV Community**: For computer vision tools and libraries
- **Python Community**: For the amazing ecosystem of packages

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/virtual-mouse/issues) page
2. Create a new issue with detailed information
3. Join the discussion in existing issues

## 🌟 Show Your Support

If you find this project helpful, please consider:

- ⭐ Starring the repository
- 🍴 Forking and contributing
- 📢 Sharing with others
- 🐛 Reporting bugs and suggesting features

---

**Made with ❤️ and Python**

_Bringing the future of human-computer interaction to your fingertips!_
