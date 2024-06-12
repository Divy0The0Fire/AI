from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

class LLM:
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    def __init__(self,
            messages: list[dict[str, str]] = [],
            model: str = "llama3-70b-8192",
            temperature: float = 0.0,
            system_prompt: str = "",
            max_tokens: int = 2048,
            connectors: list[str] = [],
            verbose: bool = False,
            api_key:str|None = None
            ):
        self.api_key = api_key if api_key else os.getenv("GROQ_API_KEY")
        self.gr = Groq(api_key = self.api_key)
        self.messages = messages
        self.model = model
        self.temperature = temperature
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.connectors = connectors
        self.verbose = verbose
        self.client = Groq(api_key=api_key)
        self.add_message(self.SYSTEM, self.system_prompt)

    def run(self, prompt: str) -> str:
        self.add_message(self.USER, prompt)
        stream = self.gr.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=self.messages,
            stream=True,
            stop=None
        )
        self.messages.pop()
        r=""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                r += chunk.choices[0].delta.content
            if self.verbose:
                print(chunk.choices[0].delta.content or "", end="")
        return r

    def add_message(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})
    def __getitem__(self, index) -> dict[str, str]|list[dict[str, str]]:
        """
        Get a message from the list of messages

        Parameters
        ----------
        index : int
            The index of the message to get

        Returns
        -------
        dict
            The message at the specified index

        Examples
        --------
        >>> llm[0]
        {'role': 'User', 'message': 'Hello, how are you?'}
        >>> llm[1]
        {'role': 'Chatbot', 'message': "I'm doing well, thank you!"}

        Raises
        ------
        TypeError
            If the index is not an integer or a slice
        """
        if isinstance(index, slice):
            return self.messages[index]
        elif isinstance(index, int):
            return self.messages[index]
        else:
            raise TypeError("Invalid argument type")

    def __setitem__(self, index, value) -> None:
        """
        Set a message in the list of messages

        Parameters
        ----------
        index : int
            The index of the message to set
        value : dict
            The new message

        Returns
        -------
        None

        Examples
        --------
        >>> llm[0] = {'role': 'User', 'message': 'Hello, how are you?'}
        >>> llm[1] = {'role': 'Chatbot', 'message': "I'm doing well, thank you!"}

        Raises
        ------
        TypeError
            If the index is not an integer or a slice
        """
        if isinstance(index, slice):
            self.messages[index] = value
        elif isinstance(index, int):
            self.messages[index] = value
        else:
            raise TypeError("Invalid argument type")
    

if __name__ == "__main__":
    llm = LLM()
    llm.add_message(LLM.USER, "Hello, how are you?")
    print(llm.run("Hello, how are you?"))
    print(llm[0])