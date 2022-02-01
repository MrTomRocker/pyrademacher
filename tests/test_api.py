import asyncio
import json
from aiohttp.cookiejar import CookieJar
from aioresponses import CallbackResult, aioresponses
import pytest
from homepilot.api import AuthError, CannotConnect, HomePilotApi

TEST_HOST = "test_host"
TEST_PASSWORD = "test_password"


class TestHomePilotApi:
    def test_init(self):
        test_instance: HomePilotApi = HomePilotApi(TEST_HOST, TEST_PASSWORD)
        assert test_instance.host == TEST_HOST
        assert test_instance.password == TEST_PASSWORD
        assert not test_instance.authenticated
        assert test_instance.cookie_jar is None

    def test_test_connection(self):
        TEST_HOST = "test_host"

        loop = asyncio.get_event_loop()
        assert loop.run_until_complete(HomePilotApi.test_connection("localhost")) == "error"

        with aioresponses() as mocked:
            mocked.get(f"http://{TEST_HOST}/", status=200, body="")
            mocked.post(f"http://{TEST_HOST}/authentication/password_salt", status=500)
            assert loop.run_until_complete(HomePilotApi.test_connection(TEST_HOST)) == "ok"

        with aioresponses() as mocked:
            mocked.get(f"http://{TEST_HOST}/", status=500, body="")
            assert loop.run_until_complete(HomePilotApi.test_connection(TEST_HOST)) == "error"

        with aioresponses() as mocked:
            mocked.get(f"http://{TEST_HOST}/", status=200, body="")
            mocked.post(f"http://{TEST_HOST}/authentication/password_salt", status=200)
            assert loop.run_until_complete(HomePilotApi.test_connection(TEST_HOST)) == "auth_required"

    def test_test_auth(self):
        TEST_HOST = "test_host"
        TEST_PASSWORD = "test_password"

        loop = asyncio.get_event_loop()

        with aioresponses() as mocked:
            with pytest.raises(AuthError):
                mocked.post(
                    f"http://{TEST_HOST}/authentication/password_salt",
                    status=500,
                    body=json.dumps({"error_code": 5007})
                )
                loop.run_until_complete(HomePilotApi.test_auth(TEST_HOST, TEST_PASSWORD))

        with aioresponses() as mocked:
            with pytest.raises(CannotConnect):
                mocked.post(
                    f"http://{TEST_HOST}/authentication/password_salt",
                    status=200,
                    body=json.dumps({"error_code": 5007})
                )
                loop.run_until_complete(HomePilotApi.test_auth(TEST_HOST, TEST_PASSWORD))

        with aioresponses() as mocked:
            with pytest.raises(AuthError):
                mocked.post(
                    f"http://{TEST_HOST}/authentication/password_salt",
                    status=200,
                    body=json.dumps({"error_code": 0, "password_salt": "12345"})
                )
                mocked.post(
                    f"http://{TEST_HOST}/authentication/login",
                    status=500
                )
                loop.run_until_complete(HomePilotApi.test_auth(TEST_HOST, TEST_PASSWORD))

        with aioresponses() as mocked:
            mocked.post(
                f"http://{TEST_HOST}/authentication/password_salt",
                status=200,
                body=json.dumps({"error_code": 0, "password_salt": "12345"})
            )
            mocked.post(
                f"http://{TEST_HOST}/authentication/login",
                status=200,
                headers={
                    "Set-Cookie": "HPSESSION=V6EivFUCps1ItXmkymnsZLcpGJZL20keUtBAIvZxsbUaDGNP31sQ4YYxUT0XXv7P;Path=/"
                }
            )
            assert isinstance(loop.run_until_complete(HomePilotApi.test_auth(TEST_HOST, TEST_PASSWORD)), CookieJar)

    def test_async_get_devices(self):
        loop = asyncio.get_event_loop()
        with aioresponses() as mocked:
            instance: HomePilotApi = HomePilotApi(TEST_HOST, "")
            mocked.get(
                f"http://{TEST_HOST}/devices",
                status=200,
                body=json.dumps({"error_code": 0, "payload": {"devices": ["a"]}})
            )
            assert loop.run_until_complete(instance.get_devices()) == ["a"]

    def test_async_get_device(self):
        did = "1234"
        device_resp = {"capabilities": []}
        loop = asyncio.get_event_loop()
        with aioresponses() as mocked:
            instance: HomePilotApi = HomePilotApi(TEST_HOST, "")
            mocked.get(
                f"http://{TEST_HOST}/devices/{did}",
                status=200,
                body=json.dumps({"error_code": 0, "payload": {"device": device_resp}})
            )
            assert loop.run_until_complete(instance.get_device(did)) == device_resp

    def test_async_get_fw_status(self):
        loop = asyncio.get_event_loop()
        response = {"response": "response_text"}
        with aioresponses() as mocked:
            instance: HomePilotApi = HomePilotApi(TEST_HOST, "")
            mocked.get(
                f"http://{TEST_HOST}/service/system-update-image/status",
                status=200,
                body=json.dumps(response)
            )
            assert loop.run_until_complete(instance.async_get_fw_status()) == response

    def test_async_get_fw_version(self):
        loop = asyncio.get_event_loop()
        response = {"response": "response_text"}
        with aioresponses() as mocked:
            instance: HomePilotApi = HomePilotApi(TEST_HOST, "")
            mocked.get(
                f"http://{TEST_HOST}/service/system-update-image/version",
                status=200,
                body=json.dumps(response)
            )
            assert loop.run_until_complete(instance.async_get_fw_version()) == response

    def test_async_get_nodename(self):
        loop = asyncio.get_event_loop()
        response = {"response": "response_text"}
        with aioresponses() as mocked:
            instance: HomePilotApi = HomePilotApi(TEST_HOST, "")
            mocked.get(
                f"http://{TEST_HOST}/service/system/networkmgr/v1/nodename",
                status=200,
                body=json.dumps(response)
            )
            assert loop.run_until_complete(instance.async_get_nodename()) == response

    def test_async_get_led_status(self):
        loop = asyncio.get_event_loop()
        response = {"response": "response_text"}
        with aioresponses() as mocked:
            instance: HomePilotApi = HomePilotApi(TEST_HOST, "")
            mocked.get(
                f"http://{TEST_HOST}/service/system/leds/status",
                status=200,
                body=json.dumps(response)
            )
            assert loop.run_until_complete(instance.async_get_led_status()) == response

    def test_async_get_devices_state(self):
        loop = asyncio.get_event_loop()
        response_actuators = {"response": "get_visible_devices", "devices": [{"did": "1", "name": "name1"}]}
        response_sensors = {"response": "get_meters", "meters": [{"did": "2", "name": "name2"}]}
        with aioresponses() as mocked:
            instance: HomePilotApi = HomePilotApi(TEST_HOST, "")
            mocked.get(
                f"http://{TEST_HOST}/v4/devices?devtype=Actuator",
                status=200,
                body=json.dumps(response_actuators)
            )
            mocked.get(
                f"http://{TEST_HOST}/v4/devices?devtype=Sensor",
                status=200,
                body=json.dumps(response_sensors)
            )
            expected = {"1": {"did": "1", "name": "name1"}, "2": {"did": "2", "name": "name2"}}
            assert loop.run_until_complete(instance.async_get_devices_state()) == expected

    def callback_ping(self, url, **kwargs):
        response = {"error_code": 0, "error_description": "OK", "payload": {}}
        return CallbackResult(
            body=json.dumps(response)
            if kwargs["json"] == {"name": "PING_CMD"}
            else json.dumps({"error_code": 20})
        )

    def test_async_ping(self):
        did = "1234"
        loop = asyncio.get_event_loop()
        with aioresponses() as mocked:
            instance: HomePilotApi = HomePilotApi(TEST_HOST, "")
            mocked.put(
                f"http://{TEST_HOST}/devices/{did}",
                status=200,
                callback=self.callback_ping
            )
            assert loop.run_until_complete(instance.async_ping(did))["error_code"] == 0

    def callback_pos_up(self, url, **kwargs):
        response = {"error_code": 0, "error_description": "OK", "payload": {}}
        return CallbackResult(
            body=json.dumps(response)
            if kwargs["json"] == {"name": "POS_UP_CMD"}
            else json.dumps({"error_code": 20})
        )

    def test_async_open_cover(self):
        did = "1234"
        loop = asyncio.get_event_loop()
        with aioresponses() as mocked:
            instance: HomePilotApi = HomePilotApi(TEST_HOST, "")
            mocked.put(
                f"http://{TEST_HOST}/devices/{did}",
                status=200,
                callback=self.callback_pos_up
            )
            assert loop.run_until_complete(instance.async_open_cover(did))["error_code"] == 0

    def callback_pos_down(self, url, **kwargs):
        response = {"error_code": 0, "error_description": "OK", "payload": {}}
        return CallbackResult(
            body=json.dumps(response)
            if kwargs["json"] == {"name": "POS_DOWN_CMD"}
            else json.dumps({"error_code": 20})
        )

    def test_async_close_cover(self):
        did = "1234"
        loop = asyncio.get_event_loop()
        with aioresponses() as mocked:
            instance: HomePilotApi = HomePilotApi(TEST_HOST, "")
            mocked.put(
                f"http://{TEST_HOST}/devices/{did}",
                status=200,
                callback=self.callback_pos_down
            )
            assert loop.run_until_complete(instance.async_close_cover(did))["error_code"] == 0

    def callback_stop(self, url, **kwargs):
        response = {"error_code": 0, "error_description": "OK", "payload": {}}
        return CallbackResult(
            body=json.dumps(response)
            if kwargs["json"] == {"name": "STOP_CMD"}
            else json.dumps({"error_code": 20})
        )

    def test_async_stop_cover(self):
        did = "1234"
        loop = asyncio.get_event_loop()
        with aioresponses() as mocked:
            instance: HomePilotApi = HomePilotApi(TEST_HOST, "")
            mocked.put(
                f"http://{TEST_HOST}/devices/{did}",
                status=200,
                callback=self.callback_stop
            )
            assert loop.run_until_complete(instance.async_stop_cover(did))["error_code"] == 0

    def callback_goto_pos(self, url, **kwargs):
        response = {"error_code": 0, "error_description": "OK", "payload": {}}
        return CallbackResult(
            body=json.dumps(response)
            if kwargs["json"] == {"name": "GOTO_POS_CMD", "value": 40}
            else json.dumps({"error_code": 20})
        )

    def test_async_set_cover_position(self):
        did = "1234"
        position = 40
        loop = asyncio.get_event_loop()
        with aioresponses() as mocked:
            instance: HomePilotApi = HomePilotApi(TEST_HOST, "")
            mocked.put(
                f"http://{TEST_HOST}/devices/{did}",
                status=200,
                callback=self.callback_goto_pos
            )
            assert loop.run_until_complete(instance.async_set_cover_position(did, position))["error_code"] == 0

    def callback_turn_on(self, url, **kwargs):
        response = {"error_code": 0, "error_description": "OK", "payload": {}}
        return CallbackResult(
            body=json.dumps(response)
            if kwargs["json"] == {"name": "TURN_ON_CMD"}
            else json.dumps({"error_code": 20})
        )

    def test_async_turn_on(self):
        did = "1234"
        loop = asyncio.get_event_loop()
        with aioresponses() as mocked:
            instance: HomePilotApi = HomePilotApi(TEST_HOST, "")
            mocked.put(
                f"http://{TEST_HOST}/devices/{did}",
                status=200,
                callback=self.callback_turn_on
            )
            assert loop.run_until_complete(instance.async_turn_on(did))["error_code"] == 0

    def callback_turn_off(self, url, **kwargs):
        response = {"error_code": 0, "error_description": "OK", "payload": {}}
        return CallbackResult(
            body=json.dumps(response)
            if kwargs["json"] == {"name": "TURN_OFF_CMD"}
            else json.dumps({"error_code": 20})
        )

    def test_async_turn_off(self):
        did = "1234"
        loop = asyncio.get_event_loop()
        with aioresponses() as mocked:
            instance: HomePilotApi = HomePilotApi(TEST_HOST, "")
            mocked.put(
                f"http://{TEST_HOST}/devices/{did}",
                status=200,
                callback=self.callback_turn_off
            )
            assert loop.run_until_complete(instance.async_turn_off(did))["error_code"] == 0

    def test_async_turn_led_on(self):
        loop = asyncio.get_event_loop()
        response = {"error_code": 0, "error_description": "OK", "payload": {}}
        with aioresponses() as mocked:
            instance: HomePilotApi = HomePilotApi(TEST_HOST, "")
            mocked.post(
                f"http://{TEST_HOST}/service/system/leds/enable",
                status=200,
                body=json.dumps(response)
            )
            assert loop.run_until_complete(instance.async_turn_led_on())["error_code"] == 0

    def test_async_turn_led_off(self):
        loop = asyncio.get_event_loop()
        response = {"error_code": 0, "error_description": "OK", "payload": {}}
        with aioresponses() as mocked:
            instance: HomePilotApi = HomePilotApi(TEST_HOST, "")
            mocked.post(
                f"http://{TEST_HOST}/service/system/leds/disable",
                status=200,
                body=json.dumps(response)
            )
            assert loop.run_until_complete(instance.async_turn_led_off())["error_code"] == 0
