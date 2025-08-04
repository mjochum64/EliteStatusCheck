#!/usr/bin/env python3
"""
Debug script für Inara API Probleme
"""

import asyncio
import json
from elite_status.inara_config import get_config
from elite_status.inara_client import InaraClient, InaraApiException
from elite_status.inara_models import InaraEventType

async def test_inara_config():
    """Test der Inara-Konfiguration"""
    print("=== Inara Konfiguration Test ===")
    try:
        config = get_config()
        print("✅ Konfiguration erfolgreich geladen")
        print(f"App Name: {config.app_name}")
        print(f"App Version: {config.app_version}")
        api_key_set = bool(config.api_key and config.api_key != "your_inara_api_key_here")
        print(f"API Key gesetzt: {api_key_set}")
        print(f"Base URL: {config.base_url}")
        return config
    except Exception as e:
        print(f"❌ Konfigurationsfehler: {e}")
        return None

async def test_inara_client():
    """Test des Inara-Clients"""
    print("\n=== Inara Client Test ===")
    try:
        async with InaraClient() as client:
            print("✅ Client erfolgreich erstellt")
            
            # Test mit einem einfachen Request
            print("Teste System-Factions Request für 'Sol'...")
            factions = await client.get_system_factions("Sol")
            print(f"✅ {len(factions)} Fraktionen für Sol gefunden")
            
            return True
            
    except InaraApiException as e:
        print(f"❌ Inara API Fehler: {e}")
        if hasattr(e, 'error_code'):
            print(f"   Error Code: {e.error_code}")
        return False
    except Exception as e:
        print(f"❌ Unerwarteter Fehler: {e}")
        print(f"   Fehlertyp: {type(e).__name__}")
        return False

async def test_direct_request():
    """Test eines direkten Inara API Requests"""
    print("\n=== Direkter API Request Test ===")
    try:
        config = get_config()
        async with InaraClient() as client:
            # Erstelle einen einfachen Request
            header = client._create_header()
            event = client._create_event(InaraEventType.GET_SYSTEM_FACTIONS, {"systemName": "Sol"})
            
            print("Request Header:")
            print(f"  appName: {header.appName}")
            print(f"  appVersion: {header.appVersion}")
            print(f"  APIkey: {'***' + header.APIkey[-4:] if header.APIkey else 'NICHT GESETZT'}")
            
            print("Request Event:")
            print(f"  eventName: {event.eventName}")
            print(f"  eventData: {event.eventData}")
            
            response = await client.send_events([event])
            print("✅ Request erfolgreich gesendet")
            print(f"Response Status: {response.events[0].eventStatus if response.events else 'Keine Events'}")
            
            return True
            
    except Exception as e:
        print(f"❌ Request Fehler: {e}")
        print(f"   Fehlertyp: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Hauptfunktion für Debug-Tests"""
    print("🔍 Inara API Debug Script")
    print("=" * 50)
    
    # 1. Konfiguration testen
    config = await test_inara_config()
    if not config:
        print("\n❌ Konfiguration fehlgeschlagen - kann nicht fortfahren")
        return
    
    # 2. Client testen
    client_ok = await test_inara_client()
    
    # 3. Direkter Request Test
    if not client_ok:
        direct_ok = await test_direct_request()
    
    print("\n" + "=" * 50)
    print("🏁 Debug Tests abgeschlossen")

if __name__ == "__main__":
    asyncio.run(main())