import tkinter as tk
import pyautogui
import pytesseract
import pyperclip
import pyocr 
import cv2
import numpy as np
from PIL import ImageGrab
import keyboard  # キーボードイベントを監視するためのライブラリ
import threading  # 非同期でキーイベントを監視するために使用

pyocr.tesseract.TESSERACT_CMD = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


class ScreenCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.3)  # 透明度を少し下げる
        self.start_x = self.start_y = self.end_x = self.end_y = None
        
        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self.start_x, self.start_y = event.x, event.y

    def on_drag(self, event):
        self.canvas.delete("rect")
        self.end_x, self.end_y = event.x, event.y
        self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline="black", tag="rect", fill="blue")

    def on_release(self, event):
        self.root.quit()  # 終了
        self.capture_screen()
        # self.canvas.delete("rect")  # 矩形を削除
        # print("選択が完了しました。再度選択できます。
    def capture_screen(self):
        img = pyautogui.screenshot(region=(self.start_x, self.start_y, self.end_x - self.start_x, self.end_y - self.start_y))
        # Tesseractのパス設定（Windowsの場合）
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        # OpenCVで前処理（グレースケール & 二値化）
        img_cv = np.array(img)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # OCR実行（英数字特化）
        config = "--psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        text = pytesseract.image_to_string(thresh, lang='eng', config=config)

        print("認識結果:", text)
        text = pytesseract.image_to_string(img, lang='eng')
        print(text)
        pyperclip.copy(text)


def monitor_keys():
    """Shift + スペースが押されたらスクリーンショットを開始"""
    while True:
        if keyboard.is_pressed("shift") and keyboard.is_pressed("space"):
            print("スクリーンショットを開始します...")
            root = tk.Tk()
            app = ScreenCaptureApp(root)
            root.mainloop()


if __name__ == "__main__":
    # キーボード監視を別スレッドで実行
    key_thread = threading.Thread(target=monitor_keys, daemon=True)
    key_thread.start()

    print("アプリは常時起動しています。Shift + スペースを押してスクリーンショットを開始してください。")
    while True:
        pass  # メインスレッドを終了させない
