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
    return {"OnFoot": check_flag(status.get("Flags2", 0), 0)}

@router.get("/inTaxi")
async def in_taxi():
    status = get_status_data()
    return {"InTaxi": check_flag(status.get("Flags2", 0), 1)}

@router.get("/inMulticrew")
async def in_multicrew():
    status = get_status_data()
    return {"InMulticrew": check_flag(status.get("Flags2", 0), 2)}

@router.get("/onFootInStation")
async def on_foot_in_station():
    status = get_status_data()
    return {"OnFootInStation": check_flag(status.get("Flags2", 0), 3)}

@router.get("/onFootOnPlanet")
async def on_foot_on_planet():
    status = get_status_data()
    return {"OnFootOnPlanet": check_flag(status.get("Flags2", 0), 4)}

@router.get("/aimDownSight")
async def aim_down_sight():
    status = get_status_data()
    return {"AimDownSight": check_flag(status.get("Flags2", 0), 5)}

@router.get("/lowOxygen")
async def low_oxygen():
    status = get_status_data()
    return {"LowOxygen": check_flag(status.get("Flags2", 0), 6)}

@router.get("/lowHealth")
async def low_health():
    status = get_status_data()
    return {"LowHealth": check_flag(status.get("Flags2", 0), 7)}

@router.get("/cold")
async def cold():
    status = get_status_data()
    return {"Cold": check_flag(status.get("Flags2", 0), 8)}

@router.get("/hot")
async def hot():
    status = get_status_data()
    return {"Hot": check_flag(status.get("Flags2", 0), 9)}

@router.get("/verycold")
async def very_cold():
    status = get_status_data()
    return {"VeryCold": check_flag(status.get("Flags2", 0), 10)}

@router.get("/veryhot")
async def very_hot():
    status = get_status_data()
    return {"VeryHot": check_flag(status.get("Flags2", 0), 11)}

@router.get("/glidemode")
async def glide_mode():
    status = get_status_data()
    return {"GlideMode": check_flag(status.get("Flags2", 0), 12)}

@router.get("/onFootInHangar")
async def on_foot_in_hangar():
    status = get_status_data()
    return {"OnFootInHangar": check_flag(status.get("Flags2", 0), 13)}

@router.get("/onFootSocialSpace")
async def on_foot_social_space():
    status = get_status_data()
    return {"OnFootSocialSpace": check_flag(status.get("Flags2", 0), 14)}

@router.get("/onFootExterior")
async def on_foot_exterior():
    status = get_status_data()
    return {"OnFootExterior": check_flag(status.get("Flags2", 0), 15)}

@router.get("/breathableAtmosphere")
async def breathable_atmosphere():
    status = get_status_data()
    return {"BreathableAtmosphere": check_flag(status.get("Flags2", 0), 16)}

@router.get("/telepresenceMulticrew")
async def telepresence_multicrew():
    status = get_status_data()
    return {"TelepresenceMulticrew": check_flag(status.get("Flags2", 0), 17)}

@router.get("/physicalMulticrew")
async def physical_multicrew():
    status = get_status_data()
    return {"PhysicalMulticrew": check_flag(status.get("Flags2", 0), 18)}

@router.get("/fsdHyperdriveCharging")
async def fsd_hyperdrive_charging():
    status = get_status_data()
    return {"FsdHyperdriveCharging": check_flag(status.get("Flags2", 0), 19)}

@router.get("/docked")
async def docked():
    status = get_status_data()
    return {"Docked": check_flag(status.get("Flags", 0), 0)}

@router.get("/landed")
async def landed():
    status = get_status_data()
    return {"Landed": check_flag(status.get("Flags", 0), 1)}

@router.get("/landingGearDown")
async def landing_gear_down():
    status = get_status_data()
    return {"LandingGearDown": check_flag(status.get("Flags", 0), 2)}

@router.get("/shieldsUp")
async def shields_up():
    status = get_status_data()
    return {"ShieldsUp": check_flag(status.get("Flags", 0), 3)}

@router.get("/supercruise")
async def supercruise():
    status = get_status_data()
    return {"Supercruise": check_flag(status.get("Flags", 0), 4)}

@router.get("/flightAssistOff")
async def flight_assist_off():
    status = get_status_data()
    return {"FlightAssistOff": check_flag(status.get("Flags", 0), 5)}

@router.get("/hardpointsDeployed")
async def hardpoints_deployed():
    status = get_status_data()
    return {"HardpointsDeployed": check_flag(status.get("Flags", 0), 6)}

@router.get("/inWing")
async def in_wing():
    status = get_status_data()
    return {"InWing": check_flag(status.get("Flags", 0), 7)}

@router.get("/lightsOn")
async def lights_on():
    status = get_status_data()
    return {"LightsOn": check_flag(status.get("Flags", 0), 8)}

@router.get("/cargoScoopDeployed")
async def cargo_scoop_deployed():
    status = get_status_data()
    return {"CargoScoopDeployed": check_flag(status.get("Flags", 0), 9)}

@router.get("/silentRunning")
async def silent_running():
    status = get_status_data()
    return {"SilentRunning": check_flag(status.get("Flags", 0), 10)}

@router.get("/scoopingFuel")
async def scooping_fuel():
    status = get_status_data()
    return {"ScoopingFuel": check_flag(status.get("Flags", 0), 11)}

@router.get("/srvHandbrake")
async def srv_handbrake():
    status = get_status_data()
    return {"SrvHandbrake": check_flag(status.get("Flags", 0), 12)}

@router.get("/srvUsingTurretView")
async def srv_using_turret_view():
    status = get_status_data()
    return {"SrvUsingTurretView": check_flag(status.get("Flags", 0), 13)}

@router.get("/srvTurretRetracted")
async def srv_turret_retracted():
    status = get_status_data()
    return {"SrvTurretRetracted": check_flag(status.get("Flags", 0), 14)}

@router.get("/fsdMassLocked")
async def fsd_mass_locked():
    status = get_status_data()
    return {"FsdMassLocked": check_flag(status.get("Flags", 0), 16)}

@router.get("/fsdCharging")
async def fsd_charging():
    status = get_status_data()
    return {"FsdCharging": check_flag(status.get("Flags", 0), 17)}

@router.get("/fsdCooldown")
async def fsd_cooldown():
    status = get_status_data()
    return {"FsdCooldown": check_flag(status.get("Flags", 0), 18)}

@router.get("/lowFuel")
async def low_fuel():
    status = get_status_data()
    return {"LowFuel": check_flag(status.get("Flags", 0), 19)}

@router.get("/overHeating")
async def over_heating():
    status = get_status_data()
    return {"OverHeating": check_flag(status.get("Flags", 0), 20)}

@router.get("/hasLatLong")
async def has_lat_long():
    status = get_status_data()
    return {"HasLatLong": check_flag(status.get("Flags", 0), 21)}

@router.get("/isInDanger")
async def is_in_danger():
    status = get_status_data()
    return {"IsInDanger": check_flag(status.get("Flags", 0), 22)}

@router.get("/beingInterdicted")
async def being_interdicted():
    status = get_status_data()
    return {"BeingInterdicted": check_flag(status.get("Flags", 0), 23)}

@router.get("/inMainShip")
async def in_main_ship():
    status = get_status_data()
    return {"InMainShip": check_flag(status.get("Flags", 0), 24)}

@router.get("/inFighter")
async def in_fighter():
    status = get_status_data()
    return {"InFighter": check_flag(status.get("Flags", 0), 25)}

@router.get("/inSrv")
async def in_srv():
    status = get_status_data()
    return {"InSrv": check_flag(status.get("Flags", 0), 26)}

@router.get("/hudInAnalysisMode")
async def hud_in_analysis_mode():
    status = get_status_data()
    return {"HudInAnalysisMode": check_flag(status.get("Flags", 0), 27)}

@router.get("/nightVision")
async def night_vision():
    status = get_status_data()
    return {"NightVision": check_flag(status.get("Flags", 0), 28)}

@router.get("/altitudeFromAverageRadius")
async def altitude_from_average_radius():
    status = get_status_data()
    return {"AltitudeFromAverageRadius": check_flag(status.get("Flags", 0), 29)}

@router.get("/fsdJump")
async def fsd_jump():
    status = get_status_data()
    return {"FsdJump": check_flag(status.get("Flags", 0), 30)}

@router.get("/srvHighBeam")
async def srv_high_beam():
    status = get_status_data()
    return {"SrvHighBeam": check_flag(status.get("Flags", 0), 31)}
