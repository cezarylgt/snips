from dataclasses import dataclass
import yaml
import os


@dataclass
class PromptQuestions:
    ask_alias: str = 'Set alias'
    ask_snippet: str = 'Set snippet'
    ask_description: str = 'Set description'
    ask_tags: str = "Set tags (separated by ',')"
    ask_defaults: str = "Set default arguments"


def load_prompt_questions() -> PromptQuestions:
    # p = os.path.join(os.path.dirname(__file__), 'config.yaml')
    # with open(p, encoding='utf-8') as f:
    #     config = yaml.safe_load(f)
    # return PromptQuestions(**config['prompt'])
    return PromptQuestions()
