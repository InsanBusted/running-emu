import subprocess
import xml.etree.ElementTree as ET
import tempfile
import re
import os
import time
import threading

MEMU_CONSOLE = r'"D:\Program Files\Microvirt\MEmu\MEmuConsole.exe"'
ADB = r'"D:\Program Files\Microvirt\MEmu\adb.exe"'
INSTAGRAM_PACKAGE = "com.instagram.android"

EMULATORS = [
    {"name": "MEmu", "device": "-s 127.0.0.1:21503"},
    {"name": "MEmu_5", "device": "-s 127.0.0.1:21553"},
    {"name": "MEmu_9", "device": "-s 127.0.0.1:21593"},
]

def start_emulator(name):
    subprocess.Popen(f'{MEMU_CONSOLE} {name}')
    print(f"Menjalankan emulator {name}...")
    time.sleep(25)

def is_device_online(device):
    result = subprocess.run(f'{ADB} devices', shell=True, capture_output=True, text=True)
    return device.split()[-1] in result.stdout

def launch_instagram_profile(device, username):
    cmd = (
        f'{ADB} {device} shell am start -a android.intent.action.VIEW '
        f'-d "https://www.instagram.com/{username}/" {INSTAGRAM_PACKAGE}'
    )
    subprocess.run(cmd, shell=True)
    print(f"Instagram @{username} dibuka pada {device}")
    time.sleep(7)
    
def dump_ui(device):
    remote_path = "/sdcard/window_dump.xml"
    cmd_dump = f'{ADB} {device} shell uiautomator dump {remote_path}'
    subprocess.run(cmd_dump, shell=True, check=True)
    local_tmp = tempfile.mktemp(suffix=".xml")
    cmd_pull = f'{ADB} {device} pull {remote_path} "{local_tmp}"'
    subprocess.run(cmd_pull, shell=True, check=True)
    return local_tmp

def tap(device, x, y):
    cmd = f'{ADB} {device} shell input tap {x} {y}'
    subprocess.run(cmd, shell=True, check=True)

def swipe_up(device):
    subprocess.run(f'{ADB} {device} shell input swipe 500 1500 500 1000', shell=True)
    time.sleep(1)

def read_likes_views(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    view_texts = []

    for node in root.iter('node'):
        text = node.attrib.get('text','').strip()
        if re.search(r'\d', text):
            view_texts.append(text)

    return view_texts[:10]


def main_for_emulator(emulator):
    name = emulator["name"]
    device = emulator["device"]

    start_emulator(name)

    if not is_device_online(device):
        print(f"Device {name} belum online, lewati...")
        return

    username = "berlbodycare"
    launch_instagram_profile(device, username)
    swipe_up(device)

    x_post, y_post = 131, 657
    print(f"{name}: Men-tap postingan pertama di {x_post},{y_post}")
    tap(device, x_post, y_post)
    time.sleep(3)

    x_post, y_post = 351, 664
    print(f"{name}: Men-tap Reels di {x_post},{y_post}")
    tap(device, x_post, y_post)
    time.sleep(25)

    tap(device, 43, 1246)
    time.sleep(2)

    xml2 = dump_ui(device)
    views = read_likes_views(xml2)
    print(f"{name}: Views/Likes yang ditemukan:", views)

    try:
        os.remove(xml2)
    except:
        pass

    # switch akun contoh
    tap(device, 35, 81)
    time.sleep(2)
    tap(device, 35, 81)
    time.sleep(2)
    tap(device, 643, 1254)
    time.sleep(2)

    time.sleep(5)
    launch_instagram_profile(device, username)
    swipe_up(device)

    x_post, y_post = 131, 657
    print(f"{name}: Men-tap postingan terbaru di {x_post},{y_post}")
    tap(device, x_post, y_post)
    time.sleep(3)

    x_post, y_post = 351, 664
    print(f"{name}: Men-tap Reels tengah di {x_post},{y_post}")
    tap(device, x_post, y_post)
    time.sleep(60)

    tap(device, 43, 1246)
    time.sleep(2)

    print(f"{name}: Proses selesai.")


if __name__ == "__main__":
    threads = []
    for emulator in EMULATORS:
        t = threading.Thread(target=main_for_emulator, args=(emulator,))
        t.start()
        threads.append(t)

    # Tunggu semua thread selesai
    for t in threads:
        t.join()

    print("Semua emulator selesai dijalankan.")