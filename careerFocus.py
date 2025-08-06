import pyautogui
from PIL import Image
import mss

def cari_gambar_di_layar(nama_gambar_template, nomor_monitor):

    try:
        with mss.mss() as sct:
            monitors = sct.monitors
            
            if not (0 < nomor_monitor < len(monitors)):
                print(f"Error: Monitor {nomor_monitor} tidak ditemukan. Jumlah monitor yang terdeteksi: {len(monitors) - 1}")
                return None
            
            monitor_region = monitors[nomor_monitor]
            sct_img = sct.grab(monitor_region)
            screenshot = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

            screenshot_rgb = screenshot.convert('RGB')

            lokasi = pyautogui.locate(nama_gambar_template, screenshot_rgb, confidence=0.8, grayscale=True)

            if lokasi:
                left, top, width, height = lokasi
                return (left + monitor_region['left'], top + monitor_region['top'], width, height)
            
            return None

    except pyautogui.ImageNotFoundException:
        print("Gambar tidak ditemukan.")
        return None
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None

# --- Contoh Penggunaan ---
if __name__ == "__main__":
    
    nama_template = "image.png"
    monitor_target = 2 

    lokasi_gambar = cari_gambar_di_layar(nama_template, monitor_target)

    if lokasi_gambar:
        print(f"{lokasi_gambar}")