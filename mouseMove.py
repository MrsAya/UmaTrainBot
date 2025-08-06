import pyautogui
import time

def pindahkan_dan_klik(x_coord, y_coord, durasi=0):
    time.sleep(1)
    pyautogui.moveTo(x_coord, y_coord, duration=durasi)
    pyautogui.click()

    print(f"Mouse telah dipindahkan dan diklik pada koordinat ({x_coord}, {y_coord}).")
