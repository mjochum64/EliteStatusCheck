Frontend-Spezifikation und Konzept: Elite Dangerous Remote Control (EDRC)

1. Einleitung
Dieses Dokument beschreibt das Konzept und die Spezifikationen für das mobile Frontend der Elite Dangerous Remote Control (EDRC). Das Frontend dient als intuitive Schnittstelle zur Steuerung von Aktionen im Spiel und zur Visualisierung des Spielstatus, wobei der Fokus auf einer schlanken Architektur und On-Device-Sprachsteuerung liegt. Das Backend (auf dem Spiele-PC) übernimmt die primäre KI-Logik, die Spielinteraktion (Tastatureingaben) und die Analyse der Log-Dateien.

2. Technologie-Stack
Entwicklungs-Framework: Flutter

Programmiersprache: Dart

Zielplattformen: iOS (primär, basierend auf deiner Erwähnung des iPhones), Android (optional für zukünftige Erweiterung)

Kommunikation mit Backend: WebSocket oder HTTP/REST (für Statusupdates und Befehlsübertragung)

3. Architektur-Ziele
Leichtgewichtiges Frontend: Minimale Logik und Datenverarbeitung auf dem Mobilgerät, Fokus auf UI/UX und Sprach-zu-Text.

Robuste Kommunikation: Zuverlässiger und effizienter Datenaustausch mit dem Backend.

Intuitive Benutzerführung: Einfache, klare Darstellung relevanter Spielinformationen und direkte Steuerungsmöglichkeiten.

Schnelle Reaktionsfähigkeit: Insbesondere bei Sprachbefehlen ist eine geringe Latenz entscheidend.

4. Kernfunktionen
4.1. Verbindung zum Backend
Statusanzeige: Visuelle Rückmeldung über den Verbindungsstatus zum Backend (z.B. "Verbunden", "Verbindungsversuch...", "Nicht verbunden").

Verbindungseinstellungen: Möglichkeit, die IP-Adresse/Port des Backend-Servers manuell einzugeben und zu speichern.

Automatische Wiederverbindung: Versuch der automatischen Wiederherstellung der Verbindung bei Unterbrechung.

4.2. Statusanzeige (Basis)
Das Frontend empfängt und zeigt ausgewählte, vom Backend bereitgestellte Statusinformationen an. Diese sollten kompakt und übersichtlich präsentiert werden.

Schiffsstatus:

Schildstatus (Prozentsatz/Balken)

Hüllenzustand (Prozentsatz/Balken)

Ziel (falls vorhanden)

Aktuelles System

Aktuelle Station/Planet

Systemstatus:

Flugmodus (Normal, FSD, Supercruise)

Fahrwerkstatus (ausgefahren/eingefahren)

Frachtlukenstatus (offen/geschlossen)

Lichterstatus (an/aus)

Ressourcen:

Treibstoff (Prozentsatz/Balken)

4.3. Manuelle Steuerung (Schaltflächen/Toggles)
Für grundlegende, einfache Aktionen, die nicht unbedingt per Sprache ausgeführt werden müssen. Diese senden direkte Befehle an das Backend.

Fahrwerk ein-/ausfahren

Frachtluke öffnen/schließen

Lichter an-/ausschalten

Landehilfe aktivieren/deaktivieren (falls vom Backend unterstützt)

Flügel/Hardpoints ein-/ausfahren (falls vom Backend unterstützt)

4.4. Sprachsteuerung (Primäre Steuerungsmethode)
Die zentrale und bevorzugte Interaktionsmethode.

Aktivierungsmodus:

"Push-to-Talk" (PTT): Taste auf dem Bildschirm, die gedrückt gehalten wird, um die Spracheingabe zu starten. Nach dem Loslassen wird die Erkennung beendet und der Befehl gesendet. (Empfohlen für Effizienz und Kontrolle).

Optional/Zukünftig: "Always Listening" mit Hotword-Erkennung (z.B. "Computer", "Elite"). Dies ist ressourcenintensiver und komplexer.

On-Device Spracherkennung: Nutzung der nativen Spracherkennungs-APIs des Mobilgeräts (z.B. SpeechRecognizer für Android, SFSpeechRecognizer für iOS) zur lokalen Umwandlung von Sprache in Text.

Textübermittlung: Der resultierende Textbefehl wird als Zeichenkette über die Kommunikationsschnittstelle an das Backend gesendet.

Visuelles Feedback: Anzeige des erkannten Textes auf dem Bildschirm, um dem Benutzer eine Rückmeldung über die Erkennung zu geben.

Fehlerrückmeldung: Bei Erkennungsfehlern oder unbekannten Befehlen kann das Frontend eine entsprechende Nachricht anzeigen (z.B. "Befehl nicht verstanden").

5. Technische Spezifikationen
5.1. Kommunikationsprotokoll
Primär: WebSockets für Echtzeit-Statusupdates vom Backend zum Frontend und für schnelle Befehlsübermittlung vom Frontend zum Backend.

Vorteile: Bidirektional, geringe Latenz, effizient für kontinuierliche Datenströme.

Fallback/Ergänzung: REST-APIs über HTTP für initiale Konfiguration oder weniger zeitkritische Anfragen (z.B. Backend-Version abfragen).

5.2. Datenformate
Alle übermittelten Daten (Statusinformationen, Befehle) sollten im JSON-Format strukturiert sein, um eine einfache Parsbarkeit auf beiden Seiten zu gewährleisten.

5.3. On-Device Spracherkennung (Flutter-spezifisch)
Verwendung des speech_to_text Flutter-Plugins (oder ähnlichem), das die nativen Plattform-APIs nutzt.

Sicherstellung der notwendigen Berechtigungen (Mikrofon).

Implementierung einer robusten Fehlerbehandlung für die Spracherkennung (z.B. bei fehlender Netzwerkverbindung für Cloud-basierte Dienste, falls nicht rein On-Device genutzt).

6. Benutzererfahrung (UX)
Klarheit und Lesbarkeit: Große Schriftarten und kontrastreiche Farben für gute Lesbarkeit im dunklen Raum.

Intuitive Anordnung: Logische Gruppierung von Statusinformationen und Steuerelementen.

Reaktionsfreudiges UI: Schnelle Reaktion auf Benutzereingaben und Statusänderungen.

Minimalistisches Design: Reduzierung auf das Wesentliche, um Überladung zu vermeiden.

7. Zukünftige Erweiterungen (Optional)
Profilverwaltung: Speichern mehrerer Backend-Verbindungsprofile.

Sprachausgabe (Text-to-Speech): Das Backend könnte Antworten an das Frontend senden, die dort vorgelesen werden (z.B. "Fahrwerk eingefahren", "Schild bei 50 Prozent").

Erweiterte KI-Schnittstelle: Visualisierung von Empfehlungen oder Analysen, die die Backend-KI generiert.

Custom Buttons/Befehle: Möglichkeit für Benutzer, eigene Befehle zu definieren.

8. Sprachgesteuerte KI-Kommunikation (Erweiterung)

Ziel: Das Frontend übernimmt die Sprache-zu-Text-Umwandlung (on-device) und sendet den erkannten Text als Klartext an das Backend. Das Backend analysiert diesen Text mittels KI/NLP und führt – sofern möglich – die gewünschte Aktion aus oder gibt eine passende Rückmeldung.

Ablauf:

Der Nutzer spricht einen Befehl (z. B. "Fahrwerk einfahren", "Lichter an").

Die App wandelt die Sprache lokal in Text um (wie bisher geplant, z. B. mit speech_to_text).

Die App sendet den Textbefehl als JSON an einen neuen Endpoint, z. B. `/api/v1/command`:

```json
{ "command": "Fahrwerk einfahren" }
```

Das Backend nutzt eine KI-Logik (z. B. OpenAI, lokale Modelle oder regelbasierte NLP), um die Absicht zu erkennen und die passende Aktion auszuführen (z. B. Fahrwerk steuern, Status abfragen, Lichter schalten).

Das Backend gibt eine strukturierte Antwort zurück, z. B.:

```json
{ "success": true, "action": "set_landing_gear", "result": "Fahrwerk eingefahren." }
```

Die App zeigt die Rückmeldung an (z. B. als Text oder optional per Sprachausgabe).

Technische Hinweise:

Die KI-Logik im Backend sollte modular aufgebaut sein, damit verschiedene Modelle/Ansätze getestet werden können.

Die API-Dokumentation ist um den neuen Endpoint `/api/v1/command` zu erweitern.

Die Sicherheit (Authentifizierung) bleibt wie gehabt.

Die App kann für die Spracheingabe weiterhin Push-to-Talk oder Always-Listening nutzen.

Vorteile:

Die App bleibt schlank und benötigt keine eigene KI-Logik.

Das Backend kann flexibel erweitert werden (z. B. neue Kommandos, komplexere Logik).

Die Sprachsteuerung ist für den Nutzer besonders intuitiv und mächtig.

---

Letzte Erweiterung: 19.07.2025