import os
import sys
import _thread
import select
import network
import socket
from machine import Pin, PWM
from time import sleep

# ========== MOTOR SETUP ==========
# Motor A
in1 = Pin(18, Pin.OUT)
in2 = Pin(19, Pin.OUT)
ena = PWM(Pin(25), freq=1000)
ena.duty(0)

# Motor B
in3 = Pin(26, Pin.OUT)
in4 = Pin(27, Pin.OUT)
enb = PWM(Pin(14), freq=1000)
enb.duty(0)

def stop():
    ena.duty(0)
    enb.duty(0)
    print("Motors stopped")

def forward():
    in1.value(1); in2.value(0); ena.duty(800)
    in3.value(1); in4.value(0); enb.duty(800)
    print("Moving forward")

def backward():
    in1.value(0); in2.value(1); ena.duty(800)
    in3.value(0); in4.value(1); enb.duty(800)
    print("Moving backward")

def left():
    in1.value(0); in2.value(1); ena.duty(800)
    in3.value(1); in4.value(0); enb.duty(800)
    print("Turning left")

def right():
    in1.value(1); in2.value(0); ena.duty(800)
    in3.value(0); in4.value(1); enb.duty(800)
    print("Turning right")

# ========== ACCESS POINT MODE ==========
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="EdgeBot-MKII", password="edgebot123", authmode=3)  # WPA2
print("Creating Wi-Fi Hotspot...")

while not ap.active():
    sleep(1)

ip = ap.ifconfig()[0]
print("Hotspot ready. Connect to: http://" + ip)

# ========== HTML INTERFACE ==========
html = """<!DOCTYPE html>
<html>
<head>
  <title>EdgeBot MK-II Control</title>
  <style>
    body { text-align: center; font-family: Arial; background: #f4f4f4; }
    h2 { color: #333; }
    .btn-grid {
      display: grid;
      grid-template-columns: repeat(3, 120px);
      gap: 15px;
      justify-content: center;
      margin-top: 30px;
    }
    .btn {
      padding: 15px;
      font-size: 18px;
      background-color: #007BFF;
      color: white;
      border: none;
      border-radius: 10px;
      box-shadow: 0 4px 6px rgba(0,0,0,0.2);
      cursor: pointer;
    }
    .btn:active {
      background-color: #0056b3;
    }
  </style>
</head>
<body>
  <h2>EdgeBot MK-II Wi-Fi Robot Controller</h2>
  <form class="btn-grid">
    <button class="btn" name="action" value="stop">STOP</button>
    <button class="btn" name="action" value="forward">FORWARD</button>
    <button class="btn" name="action" value="left">LEFT</button>
    <button class="btn" name="action" value="right">RIGHT</button>
    <button class="btn" name="action" value="backward">BACKWARD</button>
  </form>
</body>
</html>
"""

# ========== WEB SERVER ==========
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print("Web server started at: http://" + ip)

stop()  # Ensure safety on boot

def web_server_loop():
    while True:
        conn, addr = s.accept()
        client_ip = addr[0]
        print("Client connected from:", client_ip)

        request = conn.recv(1024)
        request = str(request)

        if 'forward' in request:
            forward()
        elif 'backward' in request:
            backward()
        elif 'left' in request:
            left()
        elif 'right' in request:
            right()
        elif 'stop' in request:
            stop()

        conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
        conn.send(html)
        conn.close()

# Launch web server thread
_thread.start_new_thread(web_server_loop, ())

# ========== USB SERIAL INTERFACE ==========
def read_serial_commands():
    print("DEVICE: EdgeBot MK-II\nVERSION: 1.0\nREADY")

    while True:
        try:
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                cmd = sys.stdin.readline().strip()
                if cmd == "LIST":
                    files = os.listdir()
                    print("FILES:")
                    for f in files:
                        print(" -", f)
                elif cmd.startswith("READ "):
                    filename = cmd.split(" ", 1)[1]
                    if filename in os.listdir():
                        with open(filename) as f:
                            print(f.read())
                    else:
                        print("ERROR: File not found")
                elif cmd == "ID":
                    print("DEVICE: EdgeBot MK-II\nVERSION: 1.0\nREADY")
                else:
                    print("Unknown command. Use LIST, READ <filename>, or ID")
        except Exception as e:
            print("ERROR:", e)

# Start serial command thread
_thread.start_new_thread(read_serial_commands, ())