# API-Spezifikation für Elite Dangerous Backend-Integration

## Ziel
Das Backend empfängt Kommandos von der Flutter-App und führt systemnahe Aktionen (z.B. Tastaturbefehle) für Elite Dangerous aus. Es prüft dabei den aktuellen Status und führt nur erlaubte Aktionen aus.

---

## Endpunkte

### 1. Status abfragen
- **GET /api/v1/status/parsed**
  - Gibt die wichtigsten Statusflags als boolesche Felder zurück.
  - Beispiel-Response:
    ```json
    {
      "docked": true,
      "landed": false,
      "landing_gear": true,
      "landing_gear_down": true,
      "lights": false,
      ...
    }
    ```

### 2. Aktion ausführen
- **POST /api/v1/action**
  - Führt eine Aktion im Spiel aus (z.B. Tastendruck, Hotkey, Makro).
  - Request-Body (JSON):
    ```json
    {
      "action": "toggle_landing_gear"
    }
    ```
  - Optional für gezielte Steuerung:
    ```json
    {
      "action": "set_landing_gear",
      "value": true
    }
    ```
  - Mögliche Actions (Beispiele):
    - "toggle_landing_gear"
    - "set_landing_gear" (value: true/false)
    - "toggle_lights"
    - "boost"
    - "fire_primary"
    - ...
  - Response:
    ```json
    {
      "success": true,
      "new_status": { ... }
    }
    ```

---

## Backend-Logik
- Prüft vor Ausführung, ob die Aktion im aktuellen Status erlaubt ist (z.B. Fahrwerk nur bedienen, wenn nicht "docked" oder "landed").
- Führt die Aktion systemnah aus (z.B. mit xdotool, AutoHotkey, pyautogui).
- Gibt nach Ausführung den neuen Status zurück.

---

## Sicherheit & Authentifizierung
- Optional: Authentifizierung per Token oder API-Key.
- Optional: Whitelist erlaubter Actions.

---

## Beispiel-Workflow
1. App fragt Status ab: `GET /api/v1/status/parsed`
2. App sendet Aktion: `POST /api/v1/action` mit `{ "action": "toggle_landing_gear" }`
3. Backend prüft Status, führt Aktion aus, gibt neuen Status zurück.

---

## Erweiterungen
- Unterstützung für weitere Aktionen (z.B. Makros, Sequenzen)
- Logging aller Aktionen
- WebSocket für Echtzeit-Status

---

## Hinweise
- Alle Programme (Spiel, Backend, App) laufen auf demselben Host.
- Das Backend ist für die systemnahe Ausführung verantwortlich.
- Die App ist das UI/Frontend und sendet nur Kommandos.
