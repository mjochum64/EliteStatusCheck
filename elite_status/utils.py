import os
import platform
from typing import Optional


def get_elite_dangerous_save_path() -> Optional[str]:
    """
    Gibt den Pfad zum Elite Dangerous Savegame-Verzeichnis plattformübergreifend zurück.
    Bevorzugt die Umgebungsvariable ELITE_STATUS_PATH, falls gesetzt.

    Returns:
        Optional[str]: Pfad zum Savegame-Verzeichnis oder None, falls nicht gefunden.
    """
    # 1. Nutzerdefinierte Umgebungsvariable
    custom_path = os.environ.get("ELITE_STATUS_PATH")
    if custom_path and os.path.isdir(custom_path):
        return custom_path

    # 2. Windows Standardpfad
    if platform.system() == "Windows":
        userprofile = os.environ.get("USERPROFILE")
        if userprofile:
            win_path = os.path.join(
                userprofile,
                "Saved Games",
                "Frontier Developments",
                "Elite Dangerous"
            )
            if os.path.isdir(win_path):
                return win_path

    # 3. Linux (Steam/Proton) Standardpfad
    if platform.system() == "Linux":
        home = os.path.expanduser("~")
        linux_path = os.path.join(
            home,
            ".local/share/Steam/steamapps/compatdata/359320/pfx/drive_c/users/steamuser/Saved Games/Frontier Developments/Elite Dangerous"
        )
        if os.path.isdir(linux_path):
            return linux_path

    # 4. Fallback: None
    return None
