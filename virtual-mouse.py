import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, mode=False, max_hands=1, detection_confidence=0.7, tracking_confidence=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=mode,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        if self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return img

    def get_landmark_positions(self, img, hand_num=0):
        landmarks = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_num]
            for id, lm in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks.append((id, cx, cy))
        return landmarks
    
import cv2
import numpy as np
import pyautogui
import time

class VirtualMouse:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector(max_hands=1)
        self.screen_w, self.screen_h = pyautogui.size()
        
        # Get camera dimensions
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cam_w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.cam_h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Movement area (avoid edges for better control)
        self.frame_reduction = 100
        
        # Smoothing parameters
        self.smoothening = 5
        self.prev_x, self.prev_y = 0, 0
        self.curr_x, self.curr_y = 0, 0
        
        # Control parameters
        self.movement_threshold = 5  # Lower threshold for better responsiveness
        self.click_distance = 40  # Distance between fingers for click
        self.drag_distance = 35   # Distance for drag gesture
        
        # State management
        self.is_dragging = False
        self.last_click_time = 0
        self.click_cooldown = 0.3
        
        # Position history for smoothing
        self.position_history = []
        self.history_length = 3
        
        # Gesture state tracking
        self.gesture_state = "NONE"
        self.gesture_frames = 0
        self.gesture_threshold = 3  # Frames to confirm gesture
        
        # GUI control variables
        self.always_on_top = True
        self.window_size_small = False
        self.show_landmarks = True
        
        # Disable PyAutoGUI fail-safe
        pyautogui.FAILSAFE = False

    def run(self):
        print("Virtual Mouse Started! Controls:")
        print("- Index finger up: Move cursor")
        print("- Index + Middle close: Left click")
        print("- Thumb + Index close: Right click")
        print("- Pinch (Thumb + Index) and move: Drag")
        print("\nKeyboard Controls:")
        print("- 't': Toggle always on top")
        print("- 's': Toggle small/large window")
        print("- 'l': Toggle hand landmarks")
        print("- 'q': Quit")
        
        # Create window with specific properties
        window_name = "AI Virtual Mouse"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        
        # Set initial window properties
        self._update_window_properties(window_name)
        
        while True:
            success, img = self.cap.read()
            if not success:
                break

            img = cv2.flip(img, 1)
            h, w, c = img.shape
            
            # Draw control area
            cv2.rectangle(img, (self.frame_reduction, self.frame_reduction), 
                         (w - self.frame_reduction, h - self.frame_reduction), (255, 0, 255), 2)
            
            # Find hands and draw landmarks based on setting
            img = self.detector.find_hands(img, draw=self.show_landmarks)
            landmarks = self.detector.get_landmark_positions(img)

            if landmarks:
                # Get finger positions
                x1, y1 = landmarks[8][1], landmarks[8][2]  # Index finger tip
                x2, y2 = landmarks[12][1], landmarks[12][2]  # Middle finger tip
                x4, y4 = landmarks[4][1], landmarks[4][2]   # Thumb tip
                
                # Always draw finger points for visual feedback
                cv2.circle(img, (x1, y1), 8, (255, 0, 0), cv2.FILLED)  # Index - Blue
                cv2.circle(img, (x2, y2), 8, (0, 255, 0), cv2.FILLED)  # Middle - Green
                cv2.circle(img, (x4, y4), 8, (0, 0, 255), cv2.FILLED)  # Thumb - Red

                # Check finger states
                fingers_up = self._check_fingers_up(landmarks)
                
                # Calculate distances
                index_middle_dist = np.hypot(x2 - x1, y2 - y1)
                thumb_index_dist = np.hypot(x4 - x1, y4 - y1)
                
                # Gesture detection and action
                current_gesture = self._detect_gesture(fingers_up, index_middle_dist, thumb_index_dist)
                
                # Gesture state management with frame counting for stability
                if current_gesture == self.gesture_state:
                    self.gesture_frames += 1
                else:
                    self.gesture_frames = 0
                    self.gesture_state = current_gesture
                
                # Execute actions based on confirmed gestures
                if self.gesture_frames >= self.gesture_threshold:
                    self._execute_gesture_action(current_gesture, x1, y1, x4, y4, img)
                
                # Display current gesture
                cv2.putText(img, f"Gesture: {self.gesture_state}", (20, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                # Display distances for debugging
                cv2.putText(img, f"IM: {int(index_middle_dist)}", (20, 80), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(img, f"TI: {int(thumb_index_dist)}", (150, 80), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Display status and controls
            self._draw_status_info(img, h, w)

            cv2.imshow(window_name, img)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('t'):
                self.always_on_top = not self.always_on_top
                self._update_window_properties(window_name)
                print(f"Always on top: {'ON' if self.always_on_top else 'OFF'}")
            elif key == ord('s'):
                self.window_size_small = not self.window_size_small
                self._update_window_properties(window_name)
                print(f"Window size: {'SMALL' if self.window_size_small else 'LARGE'}")
            elif key == ord('l'):
                self.show_landmarks = not self.show_landmarks
                print(f"Hand landmarks: {'ON' if self.show_landmarks else 'OFF'}")

        self.cap.release()
        cv2.destroyAllWindows()

    def _update_window_properties(self, window_name):
        """Update window properties based on current settings"""
        try:
            # Set window to stay on top or not
            if self.always_on_top:
                cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
            else:
                cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 0)
            
            # Set window size
            if self.window_size_small:
                cv2.resizeWindow(window_name, 400, 300)
                # Position window in top-right corner
                cv2.moveWindow(window_name, self.screen_w - 420, 20)
            else:
                cv2.resizeWindow(window_name, 640, 480)
                # Position window in a convenient location
                cv2.moveWindow(window_name, 50, 50)
                
        except Exception as e:
            print(f"Note: Some window properties may not be supported on this system: {e}")

    def _draw_status_info(self, img, h, w):
        """Draw status information and controls on the image"""
        # Status indicators
        status_y = h - 120
        
        # Always on top status
        top_color = (0, 255, 0) if self.always_on_top else (0, 0, 255)
        cv2.putText(img, f"OnTop: {'ON' if self.always_on_top else 'OFF'}", 
                   (20, status_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, top_color, 1)
        
        # Window size status
        size_color = (0, 255, 255) if self.window_size_small else (255, 255, 0)
        cv2.putText(img, f"Size: {'SMALL' if self.window_size_small else 'LARGE'}", 
                   (130, status_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, size_color, 1)
        
        # Landmarks status
        landmarks_color = (0, 255, 0) if self.show_landmarks else (0, 0, 255)
        cv2.putText(img, f"Landmarks: {'ON' if self.show_landmarks else 'OFF'}", 
                   (250, status_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, landmarks_color, 1)
        
        # Control instructions (more compact)
        instructions = [
            "Controls: [T]op [S]ize [L]andmarks [Q]uit",
        ]
        
        for i, instruction in enumerate(instructions):
            cv2.putText(img, instruction, (20, h - 50 + i * 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    def _check_fingers_up(self, landmarks):
        """Check which fingers are up"""
        fingers = []
        
        # Thumb (check x-coordinate relative to previous joint)
        if landmarks[4][1] > landmarks[3][1]:  # Right hand
            fingers.append(1)
        else:
            fingers.append(0)
        
        # Four fingers (check y-coordinate)
        for tip_id in [8, 12, 16, 20]:
            if landmarks[tip_id][2] < landmarks[tip_id - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers

    def _detect_gesture(self, fingers_up, index_middle_dist, thumb_index_dist):
        """Detect current gesture based on finger positions"""
        
        # Only index finger up - MOVE
        if fingers_up[1] == 1 and fingers_up[2] == 0 and fingers_up[3] == 0:
            return "MOVE"
        
        # Index and middle up, close together - LEFT CLICK
        elif (fingers_up[1] == 1 and fingers_up[2] == 1 and 
              index_middle_dist < self.click_distance):
            return "LEFT_CLICK"
        
        # Thumb and index close together - RIGHT CLICK or DRAG
        elif thumb_index_dist < self.drag_distance:
            if fingers_up[0] == 1 and fingers_up[1] == 1:
                return "DRAG"
            else:
                return "RIGHT_CLICK"
        
        return "NONE"

    def _execute_gesture_action(self, gesture, x1, y1, x4, y4, img):
        """Execute action based on detected gesture"""
        current_time = time.time()
        
        if gesture == "MOVE":
            self._handle_cursor_movement(x1, y1)
            cv2.putText(img, "MOVING", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
        elif gesture == "LEFT_CLICK":
            if (current_time - self.last_click_time) > self.click_cooldown:
                pyautogui.click()
                self.last_click_time = current_time
                cv2.putText(img, "LEFT CLICK", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
        elif gesture == "RIGHT_CLICK":
            if (current_time - self.last_click_time) > self.click_cooldown:
                pyautogui.rightClick()
                self.last_click_time = current_time
                cv2.putText(img, "RIGHT CLICK", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
        elif gesture == "DRAG":
            if not self.is_dragging:
                pyautogui.mouseDown()
                self.is_dragging = True
                cv2.putText(img, "DRAG START", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            # Use midpoint of thumb and index for drag movement
            drag_x = (x1 + x4) // 2
            drag_y = (y1 + y4) // 2
            self._handle_cursor_movement(drag_x, drag_y)
            cv2.putText(img, "DRAGGING", (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
        else:  # "NONE"
            if self.is_dragging:
                pyautogui.mouseUp()
                self.is_dragging = False
                cv2.putText(img, "DRAG END", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    def _handle_cursor_movement(self, x, y):
        """Handle smooth cursor movement with improved mapping"""
        
        # Only move if finger is within the control area
        if (x < self.frame_reduction or x > self.cam_w - self.frame_reduction or
            y < self.frame_reduction or y > self.cam_h - self.frame_reduction):
            return
        
        # Map camera coordinates to screen coordinates
        # Improved mapping that maintains aspect ratio and provides better control
        x3 = np.interp(x, (self.frame_reduction, self.cam_w - self.frame_reduction), (0, self.screen_w))
        y3 = np.interp(y, (self.frame_reduction, self.cam_h - self.frame_reduction), (0, self.screen_h))
        
        # Store position history for smoothing
        self.position_history.append((x3, y3))
        if len(self.position_history) > self.history_length:
            self.position_history.pop(0)
        
        # Calculate smoothed position
        if len(self.position_history) > 0:
            avg_x = sum(pos[0] for pos in self.position_history) / len(self.position_history)
            avg_y = sum(pos[1] for pos in self.position_history) / len(self.position_history)
        else:
            avg_x, avg_y = x3, y3
        
        # Calculate movement distance
        if self.prev_x != 0 or self.prev_y != 0:
            distance = np.hypot(avg_x - self.prev_x, avg_y - self.prev_y)
            
            # Only move if beyond threshold to avoid jitter
            if distance > self.movement_threshold:
                # Apply smoothing
                self.curr_x = self.prev_x + (avg_x - self.prev_x) / self.smoothening
                self.curr_y = self.prev_y + (avg_y - self.prev_y) / self.smoothening
                
                # Move cursor (no need to flip x-coordinate as camera is already flipped)
                pyautogui.moveTo(self.curr_x, self.curr_y)
                self.prev_x, self.prev_y = self.curr_x, self.curr_y
        else:
            # First movement
            self.prev_x, self.prev_y = avg_x, avg_y
            self.curr_x, self.curr_y = avg_x, avg_y
            pyautogui.moveTo(self.curr_x, self.curr_y)


if __name__ == "__main__":
    vm = VirtualMouse()
    vm.run()