# Hinweise für die Entwicklung der Frontend-App (EliteStatusCheck)

## Ziel
Die Frontend-App soll mit dem EliteStatusCheck-Backend kommunizieren und Aktionen (z. B. Fahrwerk steuern) sowie Statusdaten anzeigen können. Die Kommunikation erfolgt über HTTP-Requests mit Token-basierter Authentifizierung.

## API-URL
- Standard: `http://<IP-des-Backend-PCs>:8000/api/v1/`
- Beispiel für Action-Endpoint: `http://192.168.123.21:8000/api/v1/status/action`

## Authentifizierung
- Jeder geschützte Request benötigt einen Header:
  - `Authorization: Bearer <TOKEN>`
- Das Token wird im Backend in der `.env`-Datei als `ELITESTATUS_API_TOKEN` gesetzt.

## Endpunkte (Auszug)
- `GET /api/v1/status/` – Rohdaten Status
- `GET /api/v1/status/parsed` – Interpretierte Statusflags
- `POST /api/v1/status/action` – Aktion auslösen (z. B. Fahrwerk)
  - Body (JSON): `{ "action": "toggle_landing_gear" }`

## Hinweise für die App-Entwicklung
- **HTTP-Client:** Nutze z. B. `http`-Paket (Flutter/Dart) für Requests.
- **Token-Verwaltung:** Ermögliche die Eingabe/Speicherung des Tokens in der App.
- **Fehlerbehandlung:** Zeige Fehler (z. B. 401 Unauthorized, 422 Unprocessable Entity) verständlich an.
- **Statusanzeige:** Zeige Statusdaten und Flags übersichtlich an.
- **Aktionen:** Biete Buttons für Aktionen wie Fahrwerk, Lichter, etc. an.
- **Konfiguration:** API-URL und Token sollten in der App einstellbar sein.

## Beispiel-Request (Dart/Flutter)
```dart
final response = await http.post(
  Uri.parse('http://192.168.123.21:8000/api/v1/status/action'),
  headers: {
    'Authorization': 'Bearer <TOKEN>',
    'Content-Type': 'application/json',
  },
  body: jsonEncode({ 'action': 'toggle_landing_gear' }),
);
```

## Sicherheit
- Das Token ist geheim zu halten und sollte nicht im Code hardcodiert werden.
- Die Kommunikation erfolgt unverschlüsselt (HTTP). Für produktive Nutzung ggf. HTTPS-Proxy vorschalten.

## Weitere Hinweise
- Die vollständige API-Dokumentation ist unter `/api/v1/docs` auf dem Backend erreichbar.
- Bei Änderungen am Backend können neue Felder/Endpunkte hinzukommen.

---
Letzte Aktualisierung: 14.07.2025
