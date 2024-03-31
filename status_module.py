from fastapi import APIRouter
import os
import json

router = APIRouter()

def get_status_data():
    # Pfad zur status.json - stelle sicher, dass dieser Pfad auf dein System passt
    status_file_path = os.path.join(os.environ['USERPROFILE'], 'Saved Games', 'Frontier Developments', 'Elite Dangerous', 'Status.json')
    with open(status_file_path, "r") as file:
        data = json.load(file)
    return data

def check_flag(flags, bit):
    return (flags & (1 << bit)) != 0

@router.get("/onFoot")
async def on_foot():
    status = get_status_data()
    return {"onFoot": check_flag(status.get("Flags2", 0), 0)}

@router.get("/inTaxi")
async def in_taxi():
    status = get_status_data()
    return {"inTaxi": check_flag(status.get("Flags2", 0), 1)}

@router.get("/lowOxygen")
async def low_oxygen():
    status = get_status_data()
    return {"lowOxygen": check_flag(status.get("Flags2", 0), 6)}

@router.get("/cold")
async def cold():
    status = get_status_data()
    return {"cold": check_flag(status.get("Flags2", 0), 8)}

@router.get("/isDocked")
async def is_docked():
    status = get_status_data()
    return {"isDocked": check_flag(status.get("Flags", 0), 0)}

# TODO Weitere Endpunkte hinzufügen
