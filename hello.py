def main():
    print("Hello from example!")


if __name__ == "__main__":
    main()
from pynput import mouse, keyboard
from datetime import datetime
import sqlite3
import threading

# 初始化 SQLite 数据库
def init_db():
    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            event_type TEXT,
            details TEXT
        )
    """)
    conn.commit()
    conn.close()

# 将事件存储到数据库
def save_event(event_type, details):
    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO events (timestamp, event_type, details) VALUES (?, ?, ?)", (timestamp, event_type, details))
    conn.commit()
    conn.close()

# 鼠标事件处理函数
def on_mouse_move(x, y):
    details = f"Mouse moved to ({x}, {y})"
    save_event("Mouse Move", details)

def on_mouse_click(x, y, button, pressed):
    action = "Pressed" if pressed else "Released"
    details = f"Mouse {action} {button} at ({x}, {y})"
    save_event("Mouse Click", details)

def on_mouse_scroll(x, y, dx, dy):
    details = f"Mouse scrolled at ({x}, {y}) with delta ({dx}, {dy})"
    save_event("Mouse Scroll", details)

# 键盘事件处理函数
def on_key_press(key):
    try:
        details = f"Key pressed: {key.char}"
    except AttributeError:
        details = f"Special key pressed: {key}"
    save_event("Key Press", details)

def on_key_release(key):
    details = f"Key released: {key}"
    save_event("Key Release", details)
    if key == keyboard.Key.esc:  # 按下 ESC 键时退出
        return False

# 初始化数据库
init_db()

# 创建鼠标和键盘监听器
mouse_listener = mouse.Listener(
    on_move=on_mouse_move,
    on_click=on_mouse_click,
    on_scroll=on_mouse_scroll)
keyboard_listener = keyboard.Listener(
    on_press=on_key_press,
    on_release=on_key_release)

# 使用线程启动监听器
mouse_listener.start()
keyboard_listener.start()

# 等待监听器结束
mouse_listener.join()
keyboard_listener.join()