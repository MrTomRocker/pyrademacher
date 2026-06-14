# pyrademacher

Python Library to read/control devices connected to your Rademacher HomePilot (or Start2Smart) hub.

This library uses the latest REST API, so you must update your hub to the latest firmware if you want to use this library.

## Installation

Use pip to install pyrademacher lib:
```bash
pip install pyrademacher
```

## Usage

### API Class

With the HomePilotApi class you can acess the REST API directly:
```python
from homepilot.api import HomePilotApi

api = HomePilotApi("hostname", "password") # password can be empty if not defined ("")

print(asyncio.run(asyncio.run(api.get_devices()))) # get all devices

asyncio.run(api.async_open_cover(did="1")) # open cover for device id "1" (assuming it's a cover device)
```

### Manager Class

You can use the HomePilotManager helper class to more easily manage the devices:
```python
import asyncio
from homepilot.manager import HomePilotManager
from homepilot.api import HomePilotApi

api = HomePilotApi("hostname", "password") # password can be empty if not defined ("")

manager = asyncio.run(HomePilotManager.async_build_manager(api))
asyncio.run(manager.update_states())

print(manager.devices["1"].is_closed)
print(manager.devices["1"].cover_position)

print(manager.devices["-1"].fw_version) # ID -1 is reserved for the hub itself
```
Each device in manager.devices is an instance of the specific device class.

### Auto Config Devices: Commands

Every device that inherits from `HomePilotAutoConfigDevice` (covers, switches/actuators,
thermostats, lights) exposes the weather and contact commands that the hub advertises for
that device. Each command has a capability flag (`has_*_cmd`) and an awaitable method that
is a no-op when the capability is missing:

| Command | Capability flag | Method |
| --- | --- | --- |
| Sun start / stop | `has_sun_start_cmd` / `has_sun_stop_cmd` | `async_sun_start_cmd()` / `async_sun_stop_cmd()` |
| Wind start / stop | `has_wind_start_cmd` / `has_wind_stop_cmd` | `async_wind_start_cmd()` / `async_wind_stop_cmd()` |
| Rain start / stop | `has_rain_start_cmd` / `has_rain_stop_cmd` | `async_rain_start_cmd()` / `async_rain_stop_cmd()` |
| Go to dawn / dusk position | `has_goto_dawn_pos_cmd` / `has_goto_dusk_pos_cmd` | `async_goto_dawn_pos_cmd()` / `async_goto_dusk_pos_cmd()` |
| Contact open / close | `has_contact_open_cmd` / `has_contact_close_cmd` | `async_contact_open_cmd()` / `async_contact_close_cmd()` |

```python
device = manager.devices["1"]

if device.has_sun_start_cmd:
    await device.async_sun_start_cmd()   # trigger the sun command

if device.has_contact_open_cmd:
    await device.async_contact_open_cmd()
```

These devices also support the auto modes (`has_*_auto_mode` / `*_auto_mode_value` /
`async_set_*_auto_mode(...)`) for `auto`, `time`, `contact`, `wind`, `dawn`, `dusk`,
`rain` and `sun`.

They additionally expose the read-only weather program "active" states for devices
that advertise the corresponding event — `has_sun_prog_active` / `sun_prog_active_value`,
`has_wind_prog_active` / `wind_prog_active_value` and `has_rain_prog_active` /
`rain_prog_active_value` — updated on every state refresh.

### Scene Management

The library supports managing HomePilot scenes with comprehensive functionality:

```python
import asyncio
from homepilot.manager import HomePilotManager
from homepilot.api import HomePilotApi
from homepilot.scenes import SceneNotAvailableError, SceneNotManuallyExecutableError

api = HomePilotApi("hostname", "password")

# Build manager with scenes (manual executable scenes only by default)
manager = asyncio.run(HomePilotManager.async_build_manager(api))

# Include all scenes (including non-manual executable)
manager = asyncio.run(HomePilotManager.async_build_manager(api, include_non_manual_executable=True))

# Access scene properties
scene = manager.scenes["1"]  # Scene with ID "1"
print(f"Scene: {scene.name}")
print(f"Description: {scene.description}")
print(f"Enabled: {scene.is_enabled}")
print(f"Manual Executable: {scene.is_manual_executable}")
print(f"Available: {scene.available}")

# Execute scene operations with automatic validation
try:
    await scene.async_execute_scene()    # Only works if scene is available and manually executable
    await scene.async_activate_scene()   # Only works if scene is available
    await scene.async_deactivate_scene() # Only works if scene is available
except SceneNotAvailableError as e:
    print(f"Scene operation failed: {e}")
except SceneNotManuallyExecutableError as e:
    print(f"Cannot manually execute scene: {e}")

# Update scenes from API
await manager.async_update_scenes()
```