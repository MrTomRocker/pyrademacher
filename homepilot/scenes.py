from .api import HomePilotApi

class HomePilotScene:
    """HomePilot Scene"""

    _api: HomePilotApi
    _sid: int
    _name: str
    _description: str

    def __init__(
        self,
        api: HomePilotApi,
        sid: int,
        name: str,
        description: str,
    ) -> None:
        self._api = api
        self._sid = sid
        self._name = name
        self._description = description

    async def async_execute_scene(self) -> None:
        await self.api.async_execute_scene(self.sid)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description
