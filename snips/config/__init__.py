from dataclasses import dataclass


@dataclass
class PromptQuestions:
    ask_alias: str = 'Set alias'
    ask_snippet: str = 'Set snippet'
    ask_description: str = 'Set description'
    ask_tags: str = "Set tags (separated by ',')"
    ask_defaults: str = "Set default arguments"


def load_prompt_questions() -> PromptQuestions:
    return PromptQuestions()
