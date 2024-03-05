import cv2
import tkinter as tk
from tkinter import ttk
import threading
import time

class LEDBlinker:
    def __init__(self, led, caption):
        self.led = led
        self.caption = caption
        self.is_blinking = False
        self.blink_thread = threading.Thread(target=self.blink)

    def start_blinking(self):
        self.is_blinking = True
        self.blink_thread.start()

    def stop_blinking(self):
        self.is_blinking = False
        self.blink_thread.join()

    def blink(self):
        while self.is_blinking:
            self.led.configure(bg="red")
            time.sleep(0.5)
            self.led.configure(bg="white")
            time.sleep(0.5)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("LED Blinker and Webcam")

        # LED labels
        self.led1_label = ttk.Label(root, text="Light bright", font=("Helvetica", 14))
        self.led1_label.grid(row=0, column=0, padx=10, pady=10)
        self.led1 = tk.Canvas(root, width=40, height=40, bd=0, highlightthickness=0)
        self.led1.grid(row=0, column=1, padx=10, pady=10)
        self.led1_oval = self.led1.create_oval(5, 5, 35, 35, fill="orange", outline="black")  # Initially set to red

        self.led2_label = ttk.Label(root, text="Light dim", font=("Helvetica", 14))
        self.led2_label.grid(row=1, column=0, padx=10, pady=10)
        self.led2 = tk.Canvas(root, width=40, height=40, bd=0, highlightthickness=0)
        self.led2.grid(row=1, column=1, padx=10, pady=10)
        self.led2_oval = self.led2.create_oval(5, 5, 35, 35, fill="yellow", outline="black")

        self.led3_label = ttk.Label(root, text="Pothole detected", font=("Helvetica", 14))
        self.led3_label.grid(row=2, column=0, padx=10, pady=10)
        self.led3 = tk.Canvas(root, width=40, height=40, bd=0, highlightthickness=0)
        self.led3.grid(row=2, column=1, padx=10, pady=10)
        self.led3_oval = self.led3.create_oval(5, 5, 35, 35, fill="red", outline="black")


        # Webcam access button
        self.webcam_button = ttk.Button(root, text="Open Webcam", command=self.open_webcam)
        self.webcam_button.grid(row=3, column=0, pady=10)

        # Close Webcam button
        self.close_webcam_button = ttk.Button(root, text="Close Webcam", command=self.close_webcam)
        self.close_webcam_button.grid(row=3, column=1, pady=10)

        # LED blinkers
        self.led_blinker1 = LEDBlinker(self.led1, "Light bright")
        self.led_blinker2 = LEDBlinker(self.led2, "Light dim")
        self.led_blinker3 = LEDBlinker(self.led3, "Pothole detected")

        # Initially start blinking for "Light bright" LED
        self.led_blinker1.start_blinking()

    def open_webcam(self):
        self.cap = cv2.VideoCapture(0)
        self.webcam_thread = threading.Thread(target=self.show_webcam)
        self.webcam_thread.start()

    def show_webcam(self):
        while True:
            ret, frame = self.cap.read()
            cv2.imshow("Webcam", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def close_webcam(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
