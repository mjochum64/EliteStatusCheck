# Virtuelles Eingabegerät unter Linux mit Python (`uinput`)

## 🎯 Ziel

Ein Python-Backend erzeugt ein virtuelles Eingabegerät (z. B. Tastatur oder Maus) und sendet gezielt Eingaben – z. B. als Reaktion auf API- oder WebSocket-Events von einem Frontend (z. B. Flutter-App). Diese Eingaben werden vom System und Spielen (auch unter Proton/Steam) wie echte Tastaturanschläge behandelt.

---

## 📦 Voraussetzungen

### System

- Linux mit `/dev/uinput`
- Benutzer muss Zugriff auf das `uinput`-Device haben
- Kernelmodul `uinput` muss geladen sein:

```bash
sudo modprobe uinput
```

udev-Regel für Benutzerrechte:

```bash
sudo tee /etc/udev/rules.d/99-uinput.rules > /dev/null <<EOF
KERNEL=="uinput", MODE="0660", GROUP="input", OPTIONS+="static_node=uinput"
EOF

sudo udevadm control --reload-rules
sudo udevadm trigger
sudo usermod -aG input $USER
```

Danach neu einloggen oder newgrp input ausführen.


Abhängigkeit installieren:

pip install python-uinput

⚙️ Funktionsweise

Das Kernel-Modul uinput erlaubt es User-Space-Anwendungen, eigene Eingabegeräte zu simulieren.
Diese Geräte senden Ereignisse (z. B. Tastendrücke) direkt an das Linux Input Subsystem – unabhängig von X11, Wayland oder Fokus.

🧪 Beispielcode (Flask REST-Backend)

```python
import uinput
from flask import Flask, request

app = Flask(__name__)

device = uinput.Device([
    uinput.KEY_A,
    uinput.KEY_ENTER,
    uinput.KEY_LEFTCTRL,
    uinput.KEY_LEFTALT,
    uinput.KEY_F
])

@app.route("/press", methods=["POST"])
def press():
    key = request.json.get("key")
    key_map = {
        "a": uinput.KEY_A,
        "enter": uinput.KEY_ENTER,
        "ctrl+alt+f": [uinput.KEY_LEFTCTRL, uinput.KEY_LEFTALT, uinput.KEY_F]
    }

    if key not in key_map:
        return {"error": "unknown key"}, 400

    if isinstance(key_map[key], list):
        device.emit_combo(key_map[key])
    else:
        device.emit_click(key_map[key])

    return {"status": "ok"}
```

Testaufruf:

```bash
curl -X POST http://localhost:5000/press \
     -H "Content-Type: application/json" \
     -d '{"key": "a"}'
```

✅ Vorteile gegenüber xdotool

Feature	xdotool	uinput
Funktioniert mit Wayland	❌	✅
Funktioniert in Vollbildspielen	❌	✅
Layout-unabhängig (Keycodes)	❌	✅
Wird vom Spiel wie echte Hardware erkannt	❌	✅

## ⚠️ Hinweis zu Wayland
Virtuelle Eingabegeräte (uinput) werden unter Wayland aus Sicherheitsgründen nicht an laufende Anwendungen oder Spiele durchgereicht. Für Gaming/Automation ist X11 weiterhin die zuverlässigere Wahl. Unter Wayland funktionieren virtuelle Tastaturen meist nur in evtest, aber nicht in normalen Programmen oder Spielen.

🔐 Sicherheit

Zugriff auf /dev/uinput ist standardmäßig eingeschränkt.

Achte darauf, nur erlaubte Keycodes zuzulassen.

Keine offenen APIs ohne Authentifizierung bereitstellen.

🧩 Integration in dein System

Du kannst das virtuelle Eingabegerät in jedes beliebige Backend integrieren:

```text
[Flutter Frontend] → HTTP/WebSocket → [Python Backend + uinput] → Tastendruck im Spiel
```

🔍 Debugging-Tipp

Mit evtest kannst du überprüfen, ob dein virtuelles Gerät korrekt Events sendet:

```bash
sudo evtest
```

Wähle das entsprechende Gerät aus und beobachte die Tastenevents.

📚 Ressourcen

PyPI: python-uinput

Arch Wiki: uinput

Linux Header: /usr/include/linux/uinput.
