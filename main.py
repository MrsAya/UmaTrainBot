import cv2
import pytesseract
from PIL import Image
import re
import numpy as np
import os

# HANYA UNTUK PENGGUNA WINDOWS
# Sesuaikan path ini dengan lokasi instalasi Tesseract Anda
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_all_numbers_from_template_v4(main_image_path, template_path, offset_box, threshold=0.75):
    """
    Mencari semua kemunculan template dan melakukan OCR pada area yang di-offset,
    menggunakan filter manual yang lebih baik untuk menghindari duplikasi.

    Args:
        main_image_path (str): Path ke gambar utama.
        template_path (str): Path ke gambar template.
        offset_box (tuple): Offset area angka.
        threshold (float): Ambang batas kemiripan untuk deteksi template.

    Returns:
        list: Sebuah list berisi semua angka unik yang ditemukan.
    """
    try:
        print(f"--- Mulai Proses Ekstraksi (Versi 4) ---")
        print(f"Mencari semua kemunculan template '{os.path.basename(template_path)}' di gambar utama.")
        
        img_main_np = cv2.imread(main_image_path)
        img_template_np = cv2.imread(template_path)

        if img_main_np is None or img_template_np is None:
            print("ERROR: Gambar utama atau template tidak ditemukan atau tidak dapat dibaca.")
            return []

        img_main_gray = cv2.cvtColor(img_main_np, cv2.COLOR_BGR2GRAY)
        img_template_gray = cv2.cvtColor(img_template_np, cv2.COLOR_BGR2GRAY)

        w, h = img_template_gray.shape[::-1]
        result = cv2.matchTemplate(img_main_gray, img_template_gray, cv2.TM_CCOEFF_NORMED)
        
        y_loc, x_loc = np.where(result >= threshold)
        
        if len(x_loc) == 0:
            print(f"Tidak ada kemiripan di atas ambang batas {threshold}.")
            return []

        print(f"Ditemukan {len(x_loc)} koordinat mentah yang melebihi ambang batas.")

        # --- LOGIKA FILTER MANUAL YANG LEBIH BAIK ---
        all_points = sorted(list(zip(x_loc, y_loc)))
        
        # Ambang batas piksel untuk dianggap sama.
        # Anda bisa menyesuaikan nilai ini. 
        # Nilai 5 piksel adalah titik awal yang baik untuk perbedaan kecil.
        pixel_tolerance = 5 
        
        detected_coords = []
        if all_points:
            detected_coords.append(all_points[0])
            for pt in all_points[1:]:
                last_x, last_y = detected_coords[-1]
                
                # Cek apakah titik saat ini terlalu dekat dengan titik terakhir
                if abs(pt[0] - last_x) > pixel_tolerance or abs(pt[1] - last_y) > pixel_tolerance:
                    detected_coords.append(pt)
        
        if not detected_coords:
            print("Setelah penyaringan, tidak ada template yang terdeteksi.")
            return []
        
        print(f"Ditemukan {len(detected_coords)} kemunculan template yang unik setelah penyaringan.")
        
        extracted_numbers = []
        img_main_pil = Image.open(main_image_path)

        for i, (template_x, template_y) in enumerate(detected_coords):
            print(f"\n--- Memproses kemunculan ke-{i+1} ---")
            print(f"Template ditemukan pada koordinat: (x={template_x}, y={template_y})")

            x_offset, y_offset, ocr_w, ocr_h = offset_box
            ocr_area_x = template_x + x_offset
            ocr_area_y = template_y + y_offset
            
            crop_box_pil = (ocr_area_x, ocr_area_y, ocr_area_x + ocr_w, ocr_area_y + ocr_h)
            
            crop_box_pil = (
                max(0, crop_box_pil[0]),
                max(0, crop_box_pil[1]),
                min(img_main_pil.width, crop_box_pil[2]),
                min(img_main_pil.height, crop_box_pil[3])
            )

            print(f"Area untuk OCR: {crop_box_pil}")

            cropped_img = img_main_pil.crop(crop_box_pil)
            
            number_text = pytesseract.image_to_string(cropped_img, config='--psm 6').strip()
            print(f"Hasil OCR mentah: '{number_text}'")

            cleaned_number = re.sub(r'\D', '', number_text)
            
            if cleaned_number:
                final_number = int(cleaned_number)
                print(f"Angka yang berhasil diekstrak: {final_number}")
                extracted_numbers.append(final_number)
            else:
                print("Angka tidak ditemukan.")

        print(f"\n--- Selesai Proses Ekstraksi ---")
        return extracted_numbers

    except Exception as e:
        print(f"--- Terjadi Kesalahan ---")
        print(f"Terjadi kesalahan: {e}")
        return []

# --- Contoh Penggunaan ---

# Gunakan fungsi v4 yang diperbarui
image_file = 'screencareer.png'
template_file = 'statlabel.png'
offset_area_for_ocr = (-3, -20, 42, 20)
all_numbers = get_all_numbers_from_template_v4(image_file, template_file, offset_area_for_ocr, threshold=0.75)

if all_numbers:
    unique_numbers = all_numbers
    print(f"\nSemua angka unik yang berhasil diekstrak: {unique_numbers}")
else:
    print("\nTidak ada angka yang ditemukan.")