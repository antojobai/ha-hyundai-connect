# Hyundai / Kia Connect for Home Assistant

Custom Home Assistant integration for Hyundai and Kia vehicles using the official [hyundai_kia_connect_api](https://github.com/Hyundai-Kia-Connect/hyundai_kia_connect_api).

## Installation

### HACS (Custom Repository)

1. Open HACS → Integrations → Explore & Download Repositories
2. Click the three dots → Custom repositories
3. Add: `https://github.com/<your-username>/<your-repo>` (or this repo URL if public)
4. Search for **Hyundai / Kia Connect** and download
5. Restart Home Assistant

### Manual

1. Create folder: `<config_dir>/custom_components/hyundai_kia_connect/`
2. Copy all files from this repo's `custom_components/hyundai_kia_connect/` into it
3. Restart Home Assistant

## Configuration

Go to **Settings → Devices & Services → Add Integration** → search for **Hyundai / Kia Connect**.

- **Username**: Connected car account email
- **Password**: Connected car account password
- **Region**: your connected car region (US, EU, IN, AU, etc.)
- **Brand**: Hyundai or Kia
- **PIN**: Vehicle PIN from the connect app

## Supported platforms

- **Sensor** - odometer, fuel level, air temperature, energy usage, EV metrics, seat heaters, warnings
- **Binary Sensor** - doors, windows, trunk, hood, lights, defrost, climate, plug/charging states
- **Lock** - door lock / unlock
- **Climate** - remote climate start / stop with target temperature
- **Device Tracker** - vehicle GPS location
- **Services** - lock, unlock, start climate, stop climate, locate, etc.

## Notes

- This integration exposes all available endpoints returned by the API for your vehicle
- EV/PHEV entities are included and disabled by default when the vehicle is ICE; they activate automatically if your vehicle supports them
- Polling interval defaults to `hyundai_kia_connect_api` defaults; adjust config entry options if needed
