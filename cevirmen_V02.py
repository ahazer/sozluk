import time
import pyperclip
from deep_translator import GoogleTranslator
from tkinter import Tk, Label, Toplevel
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import threading

# Çevrilen kelimeleri saklamak için bir liste
translation_history = []

# Pop-up gösterme fonksiyonu
def show_popup(translation):
    root = Tk()
    root.title("Çeviri")
    root.geometry("300x100")
    root.resizable(False, False)
    label = Label(root, text=translation, wraplength=280, justify="center")
    label.pack(expand=True)
    root.after(3000, root.destroy)  # 3 saniye sonra pop-up'ı kapat
    root.mainloop()

"""# Çeviri geçmişini gösterme fonksiyonu
def show_history_popup():
    history_window = Toplevel()
    history_window.title("Çeviri Geçmişi")
    history_window.geometry("300x200")
    history_window.resizable(False, False)

    # Geçmişi birleştirerek göster
    history_text = "\n".join([f"{i+1}. {item[0]} -> {item[1]}" for i, item in enumerate(translation_history)])
    label = Label(history_window, text=history_text, wraplength=280, justify="left")
    label.pack(expand=True)"""

# Sürekli panoyu kontrol etme
def clipboard_listener():
    last_text = ""
    while True:
        try:
            # Panodan metni al
            text = pyperclip.paste()
            if text != last_text and text.strip():  # Yeni bir metin varsa
                last_text = text
                # Çeviriyi yap
                result = GoogleTranslator(source="auto", target="tr").translate(text)
                # Çeviri sonucunu göster
                show_popup(result)

                """# Çeviri geçmişine ekle (en fazla 5 öğe sakla)
                translation_history.append((text, result))
                if len(translation_history) > 5:
                    translation_history.pop(0)"""
        except Exception as e:
            print(f"Hata: {e}")
        time.sleep(1)  # 1 saniye bekle

# Sistem tepsisi simgesi oluşturma
def create_image(width, height, color1, color2):
    image = Image.new("RGB", (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 4, height // 4, width * 3 // 4, height * 3 // 4),
        fill=color2
    )
    return image

def on_quit(icon, item):
    icon.stop()
    exit(0)

"""def on_show_history(icon, item):
    # Çeviri geçmişini göster
    root = Tk()
    root.withdraw()  # Ana pencereyi gizle
    show_history_popup()"""

def start_tray_icon():
    # Sistem tepsisi menüsü
    menu = Menu(
        #MenuItem("Geçmişi Göster", on_show_history),
        MenuItem("Çıkış", on_quit)
    )
    # Simge oluşturma
    icon = Icon(
        "Çevirmen",
        create_image(64, 64, "blue", "white"),
        "Çevirmen",
        menu
    )
    icon.run()

if __name__ == "__main__":
    # Sistem tepsisi simgesini ayrı bir thread'de çalıştır
    tray_thread = threading.Thread(target=start_tray_icon, daemon=True)
    tray_thread.start()

    # Panoyu dinlemeye başla
    clipboard_listener()