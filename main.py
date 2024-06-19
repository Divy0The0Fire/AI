from plugins.codebrew import CodeBrew, codebrewPrompt, samplePrompt
from llm.ChatGpt import LLM

llm = LLM(verbose=True, max_tokens=4096, messages=samplePrompt(), system_prompt=codebrewPrompt())

while 1:
    CodeBrew(llm, keepHistory=False).run(input(">>> "))