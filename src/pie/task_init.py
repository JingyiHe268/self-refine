import pandas as pd
from src.utils import Prompt

from prompt_lib import deepseek_api


class PieInit(Prompt):
    def __init__(self, prompt_examples: str, engine: str, temperature: float) -> None:
        super().__init__(
            question_prefix="# slower version:\n",
            answer_prefix="# optimized version of the same code:\n",
            intra_example_sep="\n\n\n",
            inter_example_sep="\n\n### END ###n\n",
        )
        self.engine = engine
        self.temperature = temperature
        self.setup_prompt_from_examples_file(prompt_examples)

    def setup_prompt_from_examples_file(self, prompt_examples) -> str:
        with open(prompt_examples, "r") as f:
            self.prompt = f.read()
    
    def make_query(self, slow_code: str) -> str:
        slow_code = slow_code.strip()
        query = f"{self.prompt}{self.question_prefix}{slow_code}{self.intra_example_sep}{self.answer_prefix}"
        return query

    def __call__(self, slow_code: str) -> str:
        generation_query = self.make_query(slow_code)
        output = deepseek_api.OpenaiAPIWrapper.call(
            prompt=generation_query,
            engine=self.engine,
            max_tokens=8000,
            stop_token="### END",
            temperature=self.temperature,
        )

        generated_code = deepseek_api.OpenaiAPIWrapper.get_first_response(output)
        generated_code = deepseek_api.OpenaiAPIWrapper.get_first_response(output)
        split_words = {"### END": 0, "```python": 1, "</think>": 1, "```": 0, "code:": 1, "```llvm": 1}
        for word in split_words.keys():
            if word in generated_code:
                generated_code = generated_code.split(word)[split_words[word]].strip()
        return generated_code.strip()


def test():
    task_init = PieInit(
        prompt_examples="data/prompt/pie/init.txt",
        engine="deepseek-r1",
        temperature=0.7
    )

    slow_code = """
def sum(n):
    res = 0
    for i in range(n):
        res += i
    return res
"""
    single_line_ip = "def sum(n): res = 0; for i in range(n): res += i; return res\n\n# Optimize the above program for faster performance\n\n   |||"
    # print(task_init.prompt)
    print(task_init(slow_code))
    

if __name__ == "__main__":
    test()