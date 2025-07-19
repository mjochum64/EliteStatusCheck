"""
Modul zur Verarbeitung von Textbefehlen (NLP/Mapping) für EliteStatusCheck.
"""
from typing import Tuple, Optional

# Beispiel-Mapping: Textbefehl zu Aktion
COMMAND_MAP = {
    "fahrwerk einfahren": ("set_landing_gear", False),
    "fahrwerk ausfahren": ("set_landing_gear", True),
    "fahrwerk umschalten": ("toggle_landing_gear", None),
    "lichter an": ("set_lights", True),
    "lichter aus": ("set_lights", False),
    "lichter umschalten": ("toggle_lights", None),
    "frachtluke öffnen": ("set_cargo_scoop", True),
    "frachtluke schließen": ("set_cargo_scoop", False),
    "frachtluke umschalten": ("toggle_cargo_scoop", None),
    "landeassistent aktivieren": ("set_landing_assist", True),
    "landeassistent deaktivieren": ("set_landing_assist", False),
    "hardpoints ausfahren": ("set_hardpoints", True),
    "hardpoints einfahren": ("set_hardpoints", False),
    "hardpoints umschalten": ("toggle_hardpoints", None),
    "supercruise aktivieren": ("set_supercruise", True),
    "supercruise deaktivieren": ("set_supercruise", False),
    "fsd aktivieren": ("set_fsd", True),
    "fsd abbrechen": ("set_fsd", False),
    "nachtmodus an": ("set_night_vision", True),
    "nachtmodus aus": ("set_night_vision", False),
    "nachtmodus umschalten": ("toggle_night_vision", None),
    "analysemodus an": ("set_analysis_mode", True),
    "analysemodus aus": ("set_analysis_mode", False),
    "analysemodus umschalten": ("toggle_analysis_mode", None),
    "status anzeigen": ("show_status", None),
    "treibstoffstand anzeigen": ("show_fuel", None),
    "ziel anvisieren": ("target_next_enemy", None),
    "ziel abwählen": ("deselect_target", None),
    "systemstatus anzeigen": ("show_system_status", None),
    "aktuelles system anzeigen": ("show_current_system", None),
}

def parse_command(text: str) -> Optional[Tuple[str, Optional[bool]]]:
    """
    Analysiert einen Textbefehl und gibt die zugehörige Aktion und den Wert zurück.

    Args:
        text (str): Der erkannte Sprachbefehl.

    Returns:
        Optional[Tuple[str, Optional[bool]]]: (Aktion, Wert) oder None, wenn nicht erkannt.
    """
    normalized = text.strip().lower()
    return COMMAND_MAP.get(normalized)
