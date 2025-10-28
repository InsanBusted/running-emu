import subprocess
import time

# Path dasar
MEMU_CONSOLE = r'"D:\Program Files\Microvirt\MEmu\MEmuConsole.exe"'
ADB_PATH = r'"D:\Program Files\Microvirt\MEmu\adb.exe"'
DEVICE = "-s 127.0.0.1:21503"

subprocess.Popen(f'{MEMU_CONSOLE} MEmu')
print("🟡 Menjalankan emulator MEmu...")
time.sleep(25)

print("🟡 Membuka aplikasi Instagram...")
subprocess.run(f'{ADB_PATH} {DEVICE} shell monkey -p com.instagram.android -c android.intent.category.LAUNCHER 1')
time.sleep(8) 

username = "berlbodycare"
print(f"🟡 Membuka profil Instagram: {username}")
subprocess.run(
    fr'{ADB_PATH} {DEVICE} shell am start -a android.intent.action.VIEW -d "https://www.instagram.com/{username}/"'
)
time.sleep(8)

# Klik postingan pertama
x, y = 115, 645
print(f"Mengklik postingan pertama di posisi ({x}, {y})...")
subprocess.run(fr'{ADB_PATH} {DEVICE} shell input tap {x} {y}')
time.sleep(6)


print(f"klik postingan pertama di posisi ({x}, {y})...")
subprocess.run(fr'{ADB_PATH} {DEVICE} shell input tap {x} {y}')
time.sleep(6)

x1, y1 = 360, 600
print("like postingan")
for i in range(2):
    subprocess.run(fr'{ADB_PATH} {DEVICE} shell input tap {x1} {y1}')  
    time.sleep(0.3)  
    
time.sleep(60)
x2, y2 = 675, 830
print(f"🟢 klik postingan pertama di posisi ({x2}, {y2})...")
subprocess.run(fr'{ADB_PATH} {DEVICE} shell input tap {x2} {y2}')

    

print("✅ Postingan pertama sudah terbuka dan di-like!")
