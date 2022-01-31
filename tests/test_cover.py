import asyncio
import json
from unittest.mock import MagicMock

import pytest

from homepilot.cover import HomePilotCover


class TestHomePilotCover:
    @pytest.fixture
    def mocked_api(self):
        f = open("tests/test_files/device_cover.json")
        j = json.load(f)
        api = MagicMock()
        func_get_device = asyncio.Future()
        func_get_device.set_result(j["payload"]["device"])
        api.get_device.return_value = func_get_device
        func_open_cover = asyncio.Future()
        func_open_cover.set_result(None)
        api.async_open_cover.return_value = func_open_cover
        func_close_cover = asyncio.Future()
        func_close_cover.set_result(None)
        api.async_close_cover.return_value = func_close_cover
        func_stop_cover = asyncio.Future()
        func_stop_cover.set_result(None)
        api.async_stop_cover.return_value = func_stop_cover
        func_set_cover_position = asyncio.Future()
        func_set_cover_position.set_result(None)
        api.async_set_cover_position.return_value = func_set_cover_position
        func_ping = asyncio.Future()
        func_ping.set_result(None)
        api.async_ping.return_value = func_ping
        yield api
    
    def test_build_from_api(self, mocked_api):
        loop = asyncio.get_event_loop()
        cover = loop.run_until_complete(HomePilotCover.async_build_from_api(mocked_api,1))
        assert cover.did == "1"
        assert cover.uid == "407903_1"
        assert cover.name == "Living Room Blinds"
        assert cover.device_number == "14234511"
        assert cover.device_group == "2"
        assert cover.fw_version == "1.2-1"
        assert cover.model == "RolloTron radio beltwinder"
        assert cover.has_ping_cmd == True
        assert cover.can_set_position == True
    
    def test_update_state(self, mocked_api):
        loop = asyncio.get_event_loop()
        cover = loop.run_until_complete(HomePilotCover.async_build_from_api(mocked_api,1))
        cover.update_state({
            "statusesMap": {
                "Position": 100
            },
            "statusValid": True
        })
        assert cover.is_closed == True
        assert cover.cover_position == 0
        assert cover.is_closing == False
        assert cover.is_opening == False
        assert cover.available == True

        cover.update_state({
            "statusesMap": {
                "Position": 40
            },
            "statusValid": False
        })
        assert cover.is_closed == False
        assert cover.cover_position == 60
        assert cover.is_closing == False
        assert cover.is_opening == False
        assert cover.available == False

    def test_async_open_cover(self, mocked_api):
        loop = asyncio.get_event_loop()
        cover = loop.run_until_complete(HomePilotCover.async_build_from_api(mocked_api,1))
        loop.run_until_complete(cover.async_open_cover())
        mocked_api.async_open_cover.assert_called_with('1')

    def test_async_close_cover(self, mocked_api):
        loop = asyncio.get_event_loop()
        cover = loop.run_until_complete(HomePilotCover.async_build_from_api(mocked_api,1))
        loop.run_until_complete(cover.async_close_cover())
        mocked_api.async_close_cover.assert_called_with('1')

    def test_async_stop_cover(self, mocked_api):
        loop = asyncio.get_event_loop()
        cover = loop.run_until_complete(HomePilotCover.async_build_from_api(mocked_api,1))
        loop.run_until_complete(cover.async_stop_cover())
        mocked_api.async_stop_cover.assert_called_with('1')

    def test_async_set_cover_position(self, mocked_api):
        loop = asyncio.get_event_loop()
        cover = loop.run_until_complete(HomePilotCover.async_build_from_api(mocked_api,1))
        loop.run_until_complete(cover.async_set_cover_position(40))
        mocked_api.async_set_cover_position.assert_called_with('1', 60)

    def test_async_ping(self, mocked_api):
        loop = asyncio.get_event_loop()
        cover = loop.run_until_complete(HomePilotCover.async_build_from_api(mocked_api,1))
        loop.run_until_complete(cover.async_ping())
        mocked_api.async_ping.assert_called_with('1')
