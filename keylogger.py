import time
from pynput import keyboard
import logging
import pyautogui



class logger:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(logger, cls).__new__(cls)
            cls._instance.keylogger_instance = Keylogger()
            cls._instance.mouse_motion = Mouse_manipulation()
        return cls._instance

    log_file = "keystrokes.log"
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s  %(message)s')
    logging_instance = logging.getLogger("Keystroke_Logger")

#last edited 28-02-2024 01:30 AM
#mouse manipulation exit error. ESC key not working still

class Keylogger:
    def __init__(self):
        self.log = []

    def on_press(self, key):
        try:
            timestamp = time.time()
            key_str = key.char if hasattr(key, 'char') else str(key)
            self.log.append((timestamp, key_str))

            logger._instance.logging_instance.info(f"Key pressed: {key_str}")

        except Exception as e:
            print(f"Error: {e}")
            # Handle special keys
            key_str = str(key).replace("'", "") # Clear Representation of Special Keys

            logger._instance.logging_instance.info(f"key pressed: {key_str}")


    def on_release(self, key):
        if key == keyboard.Key.esc:
            return False

    def start_logging(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def print_log(self):
        for timestamp, key in self.log:
            print(f"{timestamp}: {key}")


class Mouse_manipulation:
    def track_mouse_movement(self):
        start_time = time.time()
        last_x, last_y = pyautogui.position()

        while True:
            current_x, current_y = pyautogui.position()
            
            if (current_x, current_y) != (last_x, last_y):
                elapsed_time = time.time() - start_time
                    
                #print(f"Time: {elapsed_time:.2f}s, X: {current_x}, Y: {current_y}")

                start_time = time.time()
                last_x, last_y = current_x, current_y

            time.sleep(0.1)  # Adjust the sleep duration based on your requirement
            
            logger._instance.logging_instance.info(f"X: {current_x}, Y: {current_y}")
    
    def on_release(self, key):
        if key == keyboard.Key.esc:
            return False


if __name__ == "__main__":
    logger_instance = logger()
    keylogger_instance = logger_instance.keylogger_instance
    mouse_motion = logger_instance.mouse_motion
    print("Press ESC to stop logging.")
    print("Keytroke Dynamics Intiated...")
    keylogger_instance.start_logging()
    keylogger_instance.print_log()
    mouse_motion = mouse_motion.track_mouse_movement()
