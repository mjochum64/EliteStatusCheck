from typing import Optional
import json
import requests
from api.interface import (
    SettingsConfig,
    WingmanConfig,
    WingmanInitializationError,
)
from api.enums import LogType, WingmanInitializationErrorType
from services.audio_player import AudioPlayer
from services.printr import Printr
from wingmen.open_ai_wingman import OpenAiWingman

printr = Printr()

class EliteWingman(OpenAiWingman):
    """Our Elite Wingman uses the EliteStatusChecker API to read the actual status information.    
    """

    def __init__(
        self,
        name: str,
        config: WingmanConfig,
        settings: SettingsConfig,
        audio_player: AudioPlayer,
    ) -> None:
        super().__init__(
            name=name, config=config, settings=settings, audio_player=audio_player
        )

        # config entry existence not validated yet. Assign later when checked!
        self.Elite_url = ""
        """The base URL of the Elite API"""

        self.headers = {"x-origin": "wingman-ai"}
        """Requireds header for the Elite API"""

        self.timeout = 5
        """Global timeout for calls to the the Elite API (in seconds)"""

        self.status_types = []

    async def validate(self):
        # collect errors from the base class (if any)
        errors: list[WingmanInitializationError] = await super().validate()

        # add custom errors
        Elite_api_url = next(
            (
                prop
                for prop in self.config.custom_properties
                if prop.id == "elite_api_url"
            ),
            None,
        )
        if not Elite_api_url or not Elite_api_url.value:
            errors.append(
                WingmanInitializationError(
                    wingman_name=self.name,
                    message="Missing required custom property 'elite_api_url'.",
                    error_type=WingmanInitializationErrorType.INVALID_CONFIG,
                )
            )
        else:
            self.Elite_url = Elite_api_url.value
            try:
                await self._prepare_data()
            except Exception as e:
                errors.append(
                    WingmanInitializationError(
                        wingman_name=self.name,
                        message=f"Failed to load data from Elite API: {e}",
                        error_type=WingmanInitializationErrorType.UNKNOWN,
                    )
                )

        return errors

    async def _prepare_data(self):
        self.start_execution_benchmark()

        self.status_types = await self._fetch_data("/")
        
    async def _fetch_data(
        self, endpoint: str, params: Optional[dict[str, any]] = None
    ) -> list[dict[str, any]]:
        url = f"{self.Elite_url}/{endpoint}"

        if self.debug:
            await printr.print_async(f"Retrieving {url}", color=LogType.INFO)

        response = requests.get(
            url, params=params, timeout=self.timeout, headers=self.headers
        )
        response.raise_for_status()
        if self.debug:
            await self.print_execution_time(reset_timer=True)

        return response.json()

    async def _execute_command_by_function_call(
        self, function_name: str, function_args: dict[str, any]
    ) -> tuple[str, str]:
        """Execute commands passed from the base class."""
        (
            function_response,
            instant_response,
        ) = await super()._execute_command_by_function_call(
            function_name, function_args
        )
        return function_response, instant_response

    def _build_tools(self) -> list[dict[str, any]]:
        """Builds the toolset for execution."""
        tools = super()._build_tools()
        return tools
