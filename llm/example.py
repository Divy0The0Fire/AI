
class LLM:
    USER = "User"
    ASSISTANT = "Chatbot"
    SYSTEM = "System"
    def __init__(
            self,
            messages: list[dict[str, str]] = [],
            model: str = "command-r-plus",
            temperature: float = 0.0,
            system_prompt: str = "",
            max_tokens: int = 2048,
            connectors: list[str] = [],
            verbose: bool = False,
            api_key:str|None = None
            ) -> None:
        """
        Initialize the LLM

        Parameters
        ----------
        messages : list[dict[str, str]], optional
            The list of messages, by default []
        model : str, optional
            The model to use, by default "command-r-plus"
        temperature : float, optional
            The temperature to use, by default 0.0
        system_prompt : str, optional
            The system prompt to use, by default ""
        max_tokens : int, optional
            The max tokens to use, by default 2048
        connectors : list[str], optional
            The connectors to use, by default []
        verbose : bool, optional
            The verbose to use, by default False
        api_key : str|None, optional
            The api key to use, by default None

        Examples
        --------
        >>> llm = LLM()
        >>> llm.add_message("User", "Hello, how are you?")
        """
        ...
    def run(self, prompt: str) -> str:
        """
        Run the LLM

        Parameters
        ----------
        prompt : str
            The prompt to run

        Returns
        -------
        str
            The response
        """
        ...
    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to the LLM

        Parameters
        ----------
        role : str
            The role of the message
        content : str
            The content of the message
        """
        ...
        
    