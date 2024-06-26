# Elite Status Check

## Beschreibung
Eine API zum Überwachen von Elite Dangerous Statusdaten.

## Verzeichnisstruktur
- main.py: Hauptdatei der Anwendung
- status_module.py: Modul zur Überwachung der Statusdateien
- cargo_module.py: Modul zur Verwaltung von Frachtdaten
- log_module.py: Modul zur Protokollierung

## Verwendung
1. Installiere die erforderlichen Bibliotheken: FastAPI, uvicorn, watchdog

    `pip install -r requirements.txt`

2. Starten der Anwendung mit: 

    `python main.py`

    oder 

    `uvicorn main:app --reload --host 0.0.0.0 --port 8888`

## Aktuell gültige Endpunkte
- `/`: Gibt den aktuellen Status, sowie das aktuelle System in einem JSON String zurück
- `/status`: Gibt den aktuellen Status zurück
- `/cargo`: Zeigt die Frachtdaten an (noch nicht implementiert!)

## Dateiüberwachung
Die Anwendung überwacht die JSON-Dateien "Status.json" und "Cargo.json" im Verzeichnis
"Saved Games/Frontier Developments/Elite Dangerous". Hier finden sich noch weitere 
Dateien, die in zukünftigen Erweiterungen folgen könnten.

## Module
### status_module.py
- Enthält Funktionen zur Verarbeitung von Statusdateien

Statusinformationen werden von Elite Dangerous in Form von 2 Bitwerten bereitgestellt,
welche alle möglichen Informationen rund um das Schiff wiedergeben.

#### Bitwert "Flags"
Dem ersten Bitwert "Flags" liegt folgende Datentabelle zu Grunde.

| Bit  | Value     | Hex        | Meaning                          |
|------|-----------|------------|----------------------------------|
| 0    | 1         | 0000 0001  | Docked, (on a landing pad)       |
| 1    | 2         | 0000 0002  | Landed, (on planet surface)      |
| 2    | 4         | 0000 0004  | Landing Gear Down                |
| 3    | 8         | 0000 0008  | Shields Up                       |
| 4    | 16        | 0000 0010  | Supercruise                      |
| 5    | 32        | 0000 0020  | FlightAssist Off                 |
| 6    | 64        | 0000 0040  | Hardpoints Deployed              |
| 7    | 128       | 0000 0080  | In Wing                          |
| 8    | 256       | 0000 0100  | LightsOn                         |
| 9    | 512       | 0000 0200  | Cargo Scoop Deployed             |
| 10   | 1024      | 0000 0400  | Silent Running,                  |
| 11   | 2048      | 0000 0800  | Scooping Fuel                    |
| 12   | 4096      | 0000 1000  | Srv Handbrake                    |
| 13   | 8192      | 0000 2000  | Srv using Turret view            |
| 14   | 16384     | 0000 4000  | Srv Turret retracted (close to ship) |
| 15   | 32768     | 0000 8000  | Srv DriveAssist                  |
| 16   | 65536     | 0001 0000  | Fsd MassLocked                   |
| 17   | 131072    | 0002 0000  | Fsd Charging                     |
| 18   | 262144    | 0004 0000  | Fsd Cooldown                     |
| 19   | 524288    | 0008 0000  | Low Fuel ( < 25% )               |
| 20   | 1048576   | 0010 0000  | Over Heating ( > 100% )          |
| 21   | 2097152   | 0020 0000  | Has Lat Long                     |
| 22   | 4194304   | 0040 0000  | IsInDanger                       |
| 23   | 8388608   | 0080 0000  | Being Interdicted                |
| 24   | 16777216  | 0100 0000  | In MainShip                      |
| 25   | 33554432  | 0200 0000  | In Fighter                       |
| 26   | 67108864  | 0400 0000  | In SRV                           |
| 27   | 134217728 | 0800 0000  | Hud in Analysis mode             |
| 28   | 268435456 | 1000 0000  | Night Vision                     |
| 29   | 536870912 | 2000 0000  | Altitude from Average radius     |
| 30   | 1073741824| 4000 0000  | fsdJump                          |
| 31   | 2147483648| 8000 0000  | srvHighBeam                      |

#### Bitwert "Flags2"
Weitere Informationen liefert der zweite Bitwert "Flags2", welcher Informationen anhand der 
folgende Datentabelle liefern kann.

| Bit | Value | Hex      | Meaning                 |
|-----|-------|----------|-------------------------|
| 0   | 1     | 0001     | OnFoot                  |
| 1   | 2     | 0002     | InTaxi (or dropship/shuttle) |
| 2   | 4     | 0004     | InMulticrew (ie in someone else's ship) |
| 3   | 8     | 0008     | OnFootInStation         |
| 4   | 16    | 0010     | OnFootOnPlanet          |
| 5   | 32    | 0020     | AimDownSight            |
| 6   | 64    | 0040     | LowOxygen               |
| 7   | 128   | 0080     | LowHealth               |
| 8   | 256   | 0100     | Cold                    |
| 9   | 512   | 0200     | Hot                     |
| 10  | 1024  | 0400     | VeryCold                |
| 11  | 2048  | 0800     | VeryHot                 |
| 12  | 4096  | 1000     | Glide Mode              |
| 13  | 8192  | 2000     | OnFootInHangar          |
| 14  | 16384 | 4000     | OnFootSocialSpace       |
| 15  | 32768 | 8000     | OnFootExterior          |
| 16  | 65536 | 0001 0000| BreathableAtmosphere    |
| 17  | 131072| 0002 0000| Telepresence Multicrew  |
| 18  | 262144| 0004 0000| Physical Multicrew      |
| 19  | 524288| 0008 0000| Fsd hyperdrive charging |

#### Beispiele für verschiedene Status Informationen

##### Im SRV
```json
{ "timestamp":"2024-03-31T15:48:54Z", "event":"Status", "Flags":69239048, "Flags2":0, "Pips":[4,4,4], "FireGroup":0, "GuiFocus":0, "Fuel":{ "FuelMain":0.000000, "FuelReservoir":0.280102 }, "Cargo":0.000000, "LegalState":"Clean", "Latitude":59.286514, "Longitude":24.757118, "Heading":10, "Altitude":0, "BodyName":"Plaa Eurk UP-X b2-0 C 3", "PlanetRadius":486614.062500, "Balance":2137875505 }
```

##### Am Boden
```json
{ "timestamp":"2024-03-31T15:52:48Z", "event":"Status", "Flags":2097152, "Flags2":33041, "Oxygen":1.000000, "Health":1.000000, "Temperature":62.468540, "SelectedWeapon":"$humanoid_fists_name;", "SelectedWeapon_Localised":"Nicht bewaffnet", "Gravity":0.041805, "LegalState":"Clean", "Latitude":59.298855, "Longitude":24.763229, "Heading":-132, "BodyName":"Plaa Eurk UP-X b2-0 C 3", "PlanetRadius":486614.062500, "Balance":2137875505 }
```

##### Im Shiff auf dem Planeten gelandet
```json
{ "timestamp":"2024-03-31T15:56:20Z", "event":"Status", "Flags":18939918, "Flags2":0, "Pips":[7,1,4], "FireGroup":3, "GuiFocus":0, "Fuel":{ "FuelMain":29.860001, "FuelReservoir":0.864660 }, "Cargo":0.000000, "LegalState":"Clean", "Latitude":59.339031, "Longitude":24.780336, "Heading":13, "Altitude":0, "BodyName":"Plaa Eurk UP-X b2-0 C 3", "PlanetRadius":486614.062500, "Balance":2137875505 }
```

##### Im Supercruise
```json
{ "timestamp":"2024-03-31T15:57:52Z", "event":"Status", "Flags":555745304, "Flags2":0, "Pips":[7,1,4], "FireGroup":3, "GuiFocus":0, "Fuel":{ "FuelMain":29.860001, "FuelReservoir":0.805023 }, "Cargo":0.000000, "LegalState":"Clean", "Latitude":59.470039, "Longitude":24.790773, "Heading":306, "Altitude":13540, "BodyName":"Plaa Eurk UP-X b2-0 C 3", "PlanetRadius":486614.062500, "Balance":2137875505 }
```

```json
{ "timestamp":"2024-03-31T16:28:22Z", "event":"Status", "Flags":155189336, "Flags2":0, "Pips":[2,8,2], "FireGroup":3, "GuiFocus":0, "Fuel":{ "FuelMain":32.000000, "FuelReservoir":0.264118 }, "Cargo":0.000000, "LegalState":"Clean", "Balance":2137875505, "Destination":{ "System":649748751449, "Body":0, "Name":"Plaa Eurk WT-I b10-0" } }
```

##### Im Hyperspace
```json
{ "timestamp":"2024-03-31T16:02:24Z", "event":"Status", "Flags":1090650136, "Flags2":524288, "Pips":[7,1,4], "FireGroup":3, "GuiFocus":0, "Fuel":{ "FuelMain":23.455589, "FuelReservoir":0.544804 }, "Cargo":0.000000, "LegalState":"Clean", "Balance":2137875505, "Destination":{ "System":646259287065, "Body":0, "Name":"Plaa Eurk XK-X b2-0" } }
```

##### Beispiel eines Cargo Inhalts aus Cargo.Json
```json
{ "timestamp":"2024-04-01T09:40:57Z", "event":"Cargo", "Vessel":"Ship", "Count":688, "Inventory":[ 
{ "Name":"bertrandite", "Name_Localised":"Bertrandit", "Count":688, "Stolen":0 }] }
```

### cargo_module.py
- Bietet Endpunkte zur Verwaltung von Frachtdaten **(noch nicht implementiert!)**

### log_module.py
- Implementiert Protokollierungsfunktionen

## API-Dokumentation
Die implementierten Schnittstellen können über die URL "/docs" eingesehen werden.

## Aktuelle Informationen
- **Entwickler:** [Martin Jochum]
- **Version:** 0.0.1
- **Letztes Update:** [13.04.2024]
- **Lizenz:** [MIT]
- **Kontakt:** [mjochum64@gmail.com]
