from dataclasses import dataclass
import yaml
import os


@dataclass
class PromptQuestions:
    ask_alias: str
    ask_snippet: str
    ask_description: str
    ask_tags: str
    ask_defaults: str


def load_prompt_questions() -> PromptQuestions:
    p = os.path.join(os.path.dirname(__file__), 'config.yaml')
    with open(p, encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return PromptQuestions(**config['prompt'])
