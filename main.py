from plugins.rawdog import RawDog, Prompts
from llm.ChatGpt import LLM

llm = LLM(verbose=True, messages=Prompts())

while 1:
    RawDog(input(">>> "), llm).run(keepHistory=True)