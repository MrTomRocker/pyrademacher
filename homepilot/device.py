""" This class represents a device in HomePilot GW """

from typing import Optional, Dict, Any
from .api import HomePilotApi

from .const import (
    APICAP_AUTO_MODE_CFG,
    APICAP_TIME_AUTO_CFG,
    APICAP_CONTACT_AUTO_CFG,
    APICAP_WIND_AUTO_CFG,
    APICAP_DAWN_AUTO_CFG,
    APICAP_DUSK_AUTO_CFG,
    APICAP_RAIN_AUTO_CFG,
    APICAP_SUN_AUTO_CFG,
    APICAP_SUN_START_CMD,
    APICAP_SUN_STOP_CMD,
    APICAP_WIND_START_CMD,
    APICAP_WIND_STOP_CMD,
    APICAP_RAIN_START_CMD,
    APICAP_RAIN_STOP_CMD,
    APICAP_GOTO_DAWN_POS_CMD,
    APICAP_GOTO_DUSK_POS_CMD,
    APICAP_CONTACT_OPEN_CMD,
    APICAP_CONTACT_CLOSE_CMD,
    APICAP_SUN_PROG_ACTIVE_EVT,
    APICAP_WIND_PROG_ACTIVE_EVT,
    APICAP_RAIN_PROG_ACTIVE_EVT,
    APICAP_DEVICE_TYPE_LOC,
    APICAP_ID_DEVICE_LOC
)

class HomePilotDevice:
    """HomePilot Device"""

    _api: HomePilotApi
    _did: int
    _uid: str
    _name: str
    _device_number: str
    _model: str
    _fw_version: str
    _device_group: int
    _manufacturer: str = "Rademacher"
    _has_ping_cmd: bool
    _available: bool

    def __init__(
        self,
        api: HomePilotApi,
        did: int,
        uid: str,
        name: str,
        device_number: str,
        model: str,
        fw_version: str,
        device_group: int,
        has_ping_cmd: bool = False,
    ) -> None:
        self._api = api
        self._did = did
        self._uid = uid
        self._name = name
        self._device_number = device_number
        self._model = model
        self._fw_version = fw_version
        self._device_group = device_group
        self._has_ping_cmd = has_ping_cmd

    @staticmethod
    def get_capabilities_map(device):
        """Returns a map containing the capabilities of a device from a response of API"""
        return {
            capability["name"]: {
                "value": capability["value"] if "value" in capability else None,
                "read_only": capability["read_only"]
                if "read_only" in capability
                else None,
                "timestamp": capability["timestamp"]
                if "timestamp" in capability
                else None,
                "min_value": capability["min_value"]
                if "min_value" in capability
                else None,
                "max_value": capability["max_value"]
                if "max_value" in capability
                else None,
                "step_size": capability["step_size"]
                if "step_size" in capability
                else None,
            }
            for capability in device["capabilities"]
        }

    @staticmethod
    def get_did_type_from_json(device):
        device_map = HomePilotDevice.get_capabilities_map(device)
        return {
            "did": device_map[APICAP_ID_DEVICE_LOC]["value"],
            "type": device_map[APICAP_DEVICE_TYPE_LOC]["value"],
        }

    async def update_state(self, state, api):
        self.available = state["statusValid"]

    async def async_ping(self):
        if self.has_ping_cmd:
            await self.api.async_ping(self.did)

    @property
    def api(self) -> HomePilotApi:
        return self._api

    @property
    def did(self):
        return self._did

    @property
    def uid(self):
        return self._uid

    @property
    def name(self):
        return self._name

    @property
    def device_number(self):
        return self._device_number

    @property
    def model(self):
        return self._model

    @property
    def fw_version(self):
        return self._fw_version

    @property
    def device_group(self):
        return self._device_group

    @property
    def manufacturer(self):
        return self._manufacturer

    @property
    def has_ping_cmd(self):
        return self._has_ping_cmd

    @property
    def available(self) -> bool:
        return self._available

    @available.setter
    def available(self, available):
        self._available = available

    @property
    def extra_attributes(self):
        return None

class HomePilotAutoConfigDevice(HomePilotDevice):
    _has_auto_mode: bool
    _auto_mode_value: bool
    _has_time_auto_mode: bool
    _time_auto_mode_value: bool
    _has_contact_auto_mode: bool
    _contact_auto_mode_value: bool
    _has_wind_auto_mode: bool
    _wind_auto_mode_value: bool
    _has_dawn_auto_mode: bool
    _dawn_auto_mode_value: bool
    _has_dusk_auto_mode: bool
    _dusk_auto_mode_value: bool
    _has_rain_auto_mode: bool
    _rain_auto_mode_value: bool
    _has_sun_auto_mode: bool
    _sun_auto_mode_value: bool
    _has_sun_start_cmd: bool
    _has_sun_stop_cmd: bool
    _has_wind_start_cmd: bool
    _has_wind_stop_cmd: bool
    _has_rain_start_cmd: bool
    _has_rain_stop_cmd: bool
    _has_goto_dawn_pos_cmd: bool
    _has_goto_dusk_pos_cmd: bool
    _has_contact_open_cmd: bool
    _has_contact_close_cmd: bool
    _has_sun_prog_active: bool
    _sun_prog_active_value: bool
    _has_wind_prog_active: bool
    _wind_prog_active_value: bool
    _has_rain_prog_active: bool
    _rain_prog_active_value: bool

    def __init__(
        self,
        api: HomePilotApi,
        did: int,
        uid: str,
        name: str,
        device_number: str,
        model: str,
        fw_version: str,
        device_group: int,
        has_ping_cmd: bool = False,
        device_map: Optional[Dict[str, Any]] = None,
     ) -> None:
        super().__init__(
            api=api,
            did=did,
            uid=uid,
            name=name,
            device_number=device_number,
            model=model,
            fw_version=fw_version,
            device_group=device_group,
            has_ping_cmd=has_ping_cmd,
        )
        device_map = device_map or {}
        self._has_auto_mode = APICAP_AUTO_MODE_CFG in device_map
        self._has_time_auto_mode = APICAP_TIME_AUTO_CFG in device_map
        self._has_contact_auto_mode = APICAP_CONTACT_AUTO_CFG in device_map
        self._has_wind_auto_mode = APICAP_WIND_AUTO_CFG in device_map
        self._has_dawn_auto_mode = APICAP_DAWN_AUTO_CFG in device_map
        self._has_dusk_auto_mode = APICAP_DUSK_AUTO_CFG in device_map
        self._has_rain_auto_mode = APICAP_RAIN_AUTO_CFG in device_map
        self._has_sun_auto_mode = APICAP_SUN_AUTO_CFG in device_map
        # Weather/contact command capabilities. These are exposed by any
        # auto config device (cover, switch/actuator, thermostat) that supports
        # the corresponding command, not only covers/thermostats.
        self._has_sun_start_cmd = APICAP_SUN_START_CMD in device_map
        self._has_sun_stop_cmd = APICAP_SUN_STOP_CMD in device_map
        self._has_wind_start_cmd = APICAP_WIND_START_CMD in device_map
        self._has_wind_stop_cmd = APICAP_WIND_STOP_CMD in device_map
        self._has_rain_start_cmd = APICAP_RAIN_START_CMD in device_map
        self._has_rain_stop_cmd = APICAP_RAIN_STOP_CMD in device_map
        self._has_goto_dawn_pos_cmd = APICAP_GOTO_DAWN_POS_CMD in device_map
        self._has_goto_dusk_pos_cmd = APICAP_GOTO_DUSK_POS_CMD in device_map
        self._has_contact_open_cmd = APICAP_CONTACT_OPEN_CMD in device_map
        self._has_contact_close_cmd = APICAP_CONTACT_CLOSE_CMD in device_map
        # Weather program "active" events (read-only state)
        self._has_sun_prog_active = APICAP_SUN_PROG_ACTIVE_EVT in device_map
        self._has_wind_prog_active = APICAP_WIND_PROG_ACTIVE_EVT in device_map
        self._has_rain_prog_active = APICAP_RAIN_PROG_ACTIVE_EVT in device_map

    async def update_device_state(self, state: Dict[str, Any], device_map: Optional[Dict[str, Any]]) -> None:
        if self.has_auto_mode:
            self.auto_mode_value = (
                state["statusesMap"]["Manuellbetrieb"] == 0
                if "Manuellbetrieb" in state["statusesMap"]
                else False
            )
        device_map = device_map or {}
        if self.has_time_auto_mode:
            self.time_auto_mode_value = device_map.get(APICAP_TIME_AUTO_CFG, {}).get("value", "false") == "true"
        if self.has_contact_auto_mode:
            self.contact_auto_mode_value = device_map.get(APICAP_CONTACT_AUTO_CFG, {}).get("value", "false") == "true"
        if self.has_wind_auto_mode:
            self.wind_auto_mode_value = device_map.get(APICAP_WIND_AUTO_CFG, {}).get("value", "false") == "true"
        if self.has_dawn_auto_mode:
            self.dawn_auto_mode_value = device_map.get(APICAP_DAWN_AUTO_CFG, {}).get("value", "false") == "true"
        if self.has_dusk_auto_mode:
            self.dusk_auto_mode_value = device_map.get(APICAP_DUSK_AUTO_CFG, {}).get("value", "false") == "true"
        if self.has_rain_auto_mode:
            self.rain_auto_mode_value = device_map.get(APICAP_RAIN_AUTO_CFG, {}).get("value", "false") == "true"
        if self.has_sun_auto_mode:
            self.sun_auto_mode_value = device_map.get(APICAP_SUN_AUTO_CFG, {}).get("value", "false") == "true"
        if self.has_sun_prog_active:
            self.sun_prog_active_value = device_map.get(APICAP_SUN_PROG_ACTIVE_EVT, {}).get("value", "false") == "true"
        if self.has_wind_prog_active:
            self.wind_prog_active_value = device_map.get(APICAP_WIND_PROG_ACTIVE_EVT, {}).get("value", "false") == "true"
        if self.has_rain_prog_active:
            self.rain_prog_active_value = device_map.get(APICAP_RAIN_PROG_ACTIVE_EVT, {}).get("value", "false") == "true"

    async def async_set_auto_mode(self, auto_mode) -> None:
        await self.api.async_set_auto_mode(self.did, auto_mode)

    async def async_set_time_auto_mode(self, auto_mode) -> None:
        await self.api.async_set_time_auto_mode(self.did, auto_mode)

    async def async_set_contact_auto_mode(self, auto_mode) -> None:
        await self.api.async_set_contact_auto_mode(self.did, auto_mode)

    async def async_set_wind_auto_mode(self, auto_mode) -> None:
        await self.api.async_set_wind_auto_mode(self.did, auto_mode)

    async def async_set_dawn_auto_mode(self, auto_mode) -> None:
        await self.api.async_set_dawn_auto_mode(self.did, auto_mode)

    async def async_set_dusk_auto_mode(self, auto_mode) -> None:
        await self.api.async_set_dusk_auto_mode(self.did, auto_mode)

    async def async_set_rain_auto_mode(self, auto_mode) -> None:
        await self.api.async_set_rain_auto_mode(self.did, auto_mode)

    async def async_set_sun_auto_mode(self, auto_mode) -> None:
        await self.api.async_set_sun_auto_mode(self.did, auto_mode)

    async def async_sun_start_cmd(self) -> None:
        if self.has_sun_start_cmd:
            await self.api.async_sun_start_cmd(self.did)

    async def async_sun_stop_cmd(self) -> None:
        if self.has_sun_stop_cmd:
            await self.api.async_sun_stop_cmd(self.did)

    async def async_wind_start_cmd(self) -> None:
        if self.has_wind_start_cmd:
            await self.api.async_wind_start_cmd(self.did)

    async def async_wind_stop_cmd(self) -> None:
        if self.has_wind_stop_cmd:
            await self.api.async_wind_stop_cmd(self.did)

    async def async_rain_start_cmd(self) -> None:
        if self.has_rain_start_cmd:
            await self.api.async_rain_start_cmd(self.did)

    async def async_rain_stop_cmd(self) -> None:
        if self.has_rain_stop_cmd:
            await self.api.async_rain_stop_cmd(self.did)

    async def async_goto_dawn_pos_cmd(self) -> None:
        if self.has_goto_dawn_pos_cmd:
            await self.api.async_goto_dawn_pos_cmd(self.did)

    async def async_goto_dusk_pos_cmd(self) -> None:
        if self.has_goto_dusk_pos_cmd:
            await self.api.async_goto_dusk_pos_cmd(self.did)

    async def async_contact_open_cmd(self) -> None:
        if self.has_contact_open_cmd:
            await self.api.async_contact_open_cmd(self.did)

    async def async_contact_close_cmd(self) -> None:
        if self.has_contact_close_cmd:
            await self.api.async_contact_close_cmd(self.did)

    @property
    def has_auto_mode(self) -> bool:
        return self._has_auto_mode

    @property
    def has_time_auto_mode(self) -> bool:
        return self._has_time_auto_mode

    @property
    def has_contact_auto_mode(self) -> bool:
        return self._has_contact_auto_mode

    @property
    def has_wind_auto_mode(self) -> bool:
        return self._has_wind_auto_mode

    @property
    def has_dawn_auto_mode(self) -> bool:
        return self._has_dawn_auto_mode

    @property
    def has_dusk_auto_mode(self) -> bool:
        return self._has_dusk_auto_mode

    @property
    def has_rain_auto_mode(self) -> bool:
        return self._has_rain_auto_mode

    @property
    def has_sun_auto_mode(self) -> bool:
        return self._has_sun_auto_mode

    @property
    def has_sun_start_cmd(self) -> bool:
        return self._has_sun_start_cmd

    @property
    def has_sun_stop_cmd(self) -> bool:
        return self._has_sun_stop_cmd

    @property
    def has_wind_start_cmd(self) -> bool:
        return self._has_wind_start_cmd

    @property
    def has_wind_stop_cmd(self) -> bool:
        return self._has_wind_stop_cmd

    @property
    def has_rain_start_cmd(self) -> bool:
        return self._has_rain_start_cmd

    @property
    def has_rain_stop_cmd(self) -> bool:
        return self._has_rain_stop_cmd

    @property
    def has_goto_dawn_pos_cmd(self) -> bool:
        return self._has_goto_dawn_pos_cmd

    @property
    def has_goto_dusk_pos_cmd(self) -> bool:
        return self._has_goto_dusk_pos_cmd

    @property
    def has_contact_open_cmd(self) -> bool:
        return self._has_contact_open_cmd

    @property
    def has_contact_close_cmd(self) -> bool:
        return self._has_contact_close_cmd

    @property
    def has_sun_prog_active(self) -> bool:
        return self._has_sun_prog_active

    @property
    def sun_prog_active_value(self) -> bool:
        return self._sun_prog_active_value

    @sun_prog_active_value.setter
    def sun_prog_active_value(self, sun_prog_active_value):
        self._sun_prog_active_value = sun_prog_active_value

    @property
    def has_wind_prog_active(self) -> bool:
        return self._has_wind_prog_active

    @property
    def wind_prog_active_value(self) -> bool:
        return self._wind_prog_active_value

    @wind_prog_active_value.setter
    def wind_prog_active_value(self, wind_prog_active_value):
        self._wind_prog_active_value = wind_prog_active_value

    @property
    def has_rain_prog_active(self) -> bool:
        return self._has_rain_prog_active

    @property
    def rain_prog_active_value(self) -> bool:
        return self._rain_prog_active_value

    @rain_prog_active_value.setter
    def rain_prog_active_value(self, rain_prog_active_value):
        self._rain_prog_active_value = rain_prog_active_value

    @property
    def auto_mode_value(self) -> bool:
        return self._auto_mode_value

    @auto_mode_value.setter
    def auto_mode_value(self, auto_mode_value):
        self._auto_mode_value = auto_mode_value

    @property
    def time_auto_mode_value(self) -> bool:
        return self._time_auto_mode_value

    @time_auto_mode_value.setter
    def time_auto_mode_value(self, time_auto_mode_value):
        self._time_auto_mode_value = time_auto_mode_value

    @property
    def contact_auto_mode_value(self) -> bool:
        return self._contact_auto_mode_value

    @contact_auto_mode_value.setter
    def contact_auto_mode_value(self, contact_auto_mode_value):
        self._contact_auto_mode_value = contact_auto_mode_value

    @property
    def wind_auto_mode_value(self) -> bool:
        return self._wind_auto_mode_value

    @wind_auto_mode_value.setter
    def wind_auto_mode_value(self, wind_auto_mode_value):
        self._wind_auto_mode_value = wind_auto_mode_value

    @property
    def dawn_auto_mode_value(self) -> bool:
        return self._dawn_auto_mode_value

    @dawn_auto_mode_value.setter
    def dawn_auto_mode_value(self, dawn_auto_mode_value):
        self._dawn_auto_mode_value = dawn_auto_mode_value

    @property
    def dusk_auto_mode_value(self) -> bool:
        return self._dusk_auto_mode_value

    @dusk_auto_mode_value.setter
    def dusk_auto_mode_value(self, dusk_auto_mode_value):
        self._dusk_auto_mode_value = dusk_auto_mode_value

    @property
    def rain_auto_mode_value(self) -> bool:
        return self._rain_auto_mode_value

    @rain_auto_mode_value.setter
    def rain_auto_mode_value(self, rain_auto_mode_value):
        self._rain_auto_mode_value = rain_auto_mode_value

    @property
    def sun_auto_mode_value(self) -> bool:
        return self._sun_auto_mode_value

    @sun_auto_mode_value.setter
    def sun_auto_mode_value(self, sun_auto_mode_value):
        self._sun_auto_mode_value = sun_auto_mode_value

