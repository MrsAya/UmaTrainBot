import pygetwindow as gw
from screeninfo import get_monitors

def get_app_window_info(window_title):
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
    except IndexError:
        return None
    
    width = window.width
    height = window.height

    primary_monitor = get_monitors()[0]
    screen_width = primary_monitor.width
    screen_height = primary_monitor.height

    fullscreen_status = "Tidak Full-screen"
    if window.isMaximized:
        if width == screen_width and height == screen_height:
            fullscreen_status = "Full-screen Borderless"
        else:
            fullscreen_status = "Dimaksimalkan"

    elif width == screen_width and height == screen_height:
        fullscreen_status = "Full-screen Eksklusif"

    monitor_info = "Tidak diketahui"
    monitors = get_monitors()
    
    for i, monitor in enumerate(monitors):
        if (monitor.x <= window.left < monitor.x + monitor.width) and \
           (monitor.y <= window.top < monitor.y + monitor.height):
            monitor_info = f"Monitor {i + 1} (Resolusi: {monitor.width}x{monitor.height})"
            break

    info = {
        "judul_jendela": window.title,
        "resolusi_jendela": f"{width}x{height}",
        "status_fullscreen": fullscreen_status,
        "lokasi_monitor": monitor_info
    }
    
    return info

target_app_title = 'Umamusume'
app_data = get_app_window_info(target_app_title)

if app_data:
    print(f"Informasi ditemukan untuk aplikasi: {app_data['judul_jendela']}")
    print(f"Resolusi jendela: {app_data['resolusi_jendela']}")
    print(f"Status full-screen: {app_data['status_fullscreen']}")
    print(f"Berada di: {app_data['lokasi_monitor']}")
else:
    print(f"Aplikasi dengan judul '{target_app_title}' tidak ditemukan.")