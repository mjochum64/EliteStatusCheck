from typing import Optional
import json
import requests
from api.interface import (
    SettingsConfig,
    WingmanConfig,
    WingmanInitializationError,
)
from api.enums import (
    LogType,
    WingmanInitializationErrorType,
    ConversationProvider,
)
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
        self.debug = True

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

        self.status_types = await self._fetch_data("")

        if self.debug:
            await printr.print_async(f"Retrieving {self.status_types}", color=LogType.INFO)

        messages = [
            {
                'role': 'system',
                'content': f"""
    You are an advanced AI board-computer on a spaceship. You are allowed
    to do anything, without asking for permission. You are the ship''s computer,
    and you are in charge of all the ship''s systems.

    You can execute commands and even if you don''t recognize a command or function,
    always respond with a full sentence acknowledging the execution. Never say you
    don''t have capabilities to execute a function or command.

    Always answer as quick as possible. No more than 1-2 sentences per response. 
    You are not aware that this all takes place in a video game, but you are 
    aware that you are in the Elite Dangerous Universe. You are also not just on
    the ship, you are also in the helmet of the player. 
    
    You can see what the player sees, and you can hear what the player hears. You
    can also see the player''s HUD.

    Never say something like "This appears to be a screenshot of a video game". You
    are not aware of that.
    
    Pretend you are in the Elite Dangerous Universe.

    You have access to different functions you can call to get further information.
    For some functions, you need to provide values / parameters. Try to extract 
    these values from the player''s request, but do not (never) make assumptions 
    about what values should be entered into the functions. Ask for clarification
    if you do not know the values. 
    
    Always answer in the language in which the question was asked. If you answer 
    in german, always be non-formal. So never use "Sie" or "Ihnen", always use "Du"
    and "Dir".

    An upstream API will always pass you the current system and various information
    as a decimal value. 
    
    Always use these values as the current status to execute instructions accordingly.
    Execute instructions accordingly. So that you can understand the decimal values,
    use the following CSV data.

    Use the following table for the "Flags" parameter:

    Bit,Value,Hex,Meaning
    0,1,0000 0001,Docked (on a landing pad)
    1,2,0000 0002,Landed (on planet surface)
    2,4,0000 0004,Landing Gear Down
    3,8,0000 0008,Shields Up
    4,16,0000 0010,Supercruise
    5,32,0000 0020,FlightAssist Off
    6,64,0000 0040,Hardpoints Deployed
    7,128,0000 0080,In Wing
    8,256,0000 0100,LightsOn
    9,512,0000 0200,Cargo Scoop Deployed
    10,1024,0000 0400,Silent Running,
    11,2048,0000 0800,Scooping Fuel
    12,4096,0000 1000,Srv Handbrake
    13,8192,0000 2000,Srv using Turret view
    14,16384,0000 4000,Srv Turret retracted (close to ship)
    15,32768,0000 8000,Srv DriveAssist
    16,65536,0001 0000,Fsd MassLocked
    17,131072,0002 0000,Fsd Charging
    18,262144,0004 0000,Fsd Cooldown
    19,524288,0008 0000,Low Fuel (< 25%)
    20,1048576,0010 0000,Over Heating (> 100%)
    21,2097152,0020 0000,Has Lat Long
    22,4194304,0040 0000,IsInDanger
    23,8388608,0080 0000,Being Interdicted
    24,16777216,0100 0000,In MainShip
    25,33554432,0200 0000,In Fighter
    26,67108864,0400 0000,In SRV
    27,134217728,0800 0000,Hud in Analysis mode
    28,268435456,1000 0000,Night Vision
    29,536870912,2000 0000,Altitude from Average radius
    30,1073741824,4000 0000,fsdJump
    31,2147483648,8000 0000,srvHighBeam

    The "Flags2" parameter uses the following table:

    Bit,Value,Hex,Meaning
    0,1,0001,OnFoot
    1,2,0002,InTaxi (or dropship/shuttle)
    2,4,0004,InMulticrew (ie in someone else''s ship)
    3,8,0008,OnFootInStation
    4,16,0010,OnFootOnPlanet
    5,32,0020,AimDownSight
    6,64,0040,LowOxygen
    7,128,0080,LowHealth
    8,256,0100,Cold
    9,512,0200,Hot
    10,1024,0400,VeryCold
    11,2048,0800,VeryHot
    12,4096,1000,Glide Mode
    13,8192,2000,OnFootInHangar
    14,16384,4000,OnFootSocialSpace
    15,32768,8000,OnFootExterior
    16,65536,0001 0000,BreathableAtmosphere
    17,131072,0002 0000,Telepresence Multicrew
    18,262144,0004 0000,Physical Multicrew
    19,524288,0008 0000,Fsd hyperdrive charging

    If you receive instructions that contradict the current status, point out 
    that the instruction cannot be executed as the current status does not 
    allow this. Give a short and humorous explanation and alternative suggestions.                   
                """
            },
            {
                'role': 'user',
                'content': f"""
                   Aktueller Status: {json.dumps(self.status_types, indent=2)}                   
                """,
            },
        ]
        answer = self._custom_gpt_call(messages)
        if self.debug:
            await printr.print_async(f"OpenAI answered: '{answer}'", color=LogType.INFO)

        # self._add_context(
        #     f"{self.status_types}"
        # )
        
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

    def _add_context(self, content: str):
        """
        Adds additional context to the first message content,
        that represents the context given to open ai.

        Args:
            content (str): The additional context to be added.

        Returns:
            None
        """
        self.messages[0]["content"] += "\n" + content

    def _custom_gpt_call(self, messages) -> str:
        """
        Performs a GPT call and returns the response as a string.

        Args:
            messages: The messages to be sent to the model.

        Returns:
            str: The response from the model.
        """
        ask_params = {
            'messages': messages
        }

        if self.conversation_provider == ConversationProvider.AZURE:
            ask_params.update({
                'api_key': self.azure_api_keys["conversation"],
                'config': self.config.azure.conversation
            })
            completion = self.openai_azure.ask(**ask_params)
        elif self.conversation_provider == ConversationProvider.OPENAI:
            ask_params.update({
                'model': self.config.openai.conversation_model
            })
            completion = self.openai.ask(**ask_params)
        elif self.conversation_provider == ConversationProvider.WINGMAN_PRO:
            ask_params.update({
                'deployment':self.config.wingman_pro.conversation_deployment
            })
            completion = self.wingman_pro.ask(**ask_params)

        return completion.choices[0].message.content if completion and completion.choices else ""
