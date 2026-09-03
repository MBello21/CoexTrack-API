import httpx
from sqlalchemy import text
from ..database import get_db


async def update_vehicle_address(device_id: str, lat: float, lon: float):
    print(f"Geocoding {device_id}: {lat}, {lon}")
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(
                "https://nominatim.openstreetmap.org/reverse",
                params={"lat": lat, "lon": lon,
                        "format": "json", "addressdetails": 1},
                headers={"User-Agent": "COEXTrack/1.0"}
            )
            if res.status_code != 200:
                return
            data = res.json()
            addr = data.get("address", {})
            ref = addr.get("ref", "")
            road = addr.get("road", "")
            road_display = f"{ref} - {road}" if ref and road else ref or road
            town = addr.get("city") or addr.get(
                "town") or addr.get("village", "")
            postcode = addr.get("postcode", "")
            short = ", ".join(filter(None, [road_display, town, postcode]))
            if short:
                db = next(get_db())
                db.execute(
                    text(
                        "UPDATE vehicles SET last_address = :addr WHERE device_id = :vid"),
                    {"addr": short, "vid": device_id}
                )
                db.commit()
        except Exception as e:
            print(f"Geocode error: {e}")
