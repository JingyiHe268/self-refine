from collections import Counter
import os
from typing import Dict, Any, List, Optional, Union
from openai import OpenAI
import random
import time
import json
api_key=os.getenv("API_KEY")
base_url=os.getenv("BASE_URL")
Client=OpenAI(api_key=api_key,base_url=base_url)

class DeepseekAPIWrapper():
    @staticmethod
    def call(
        prompt: Union[str, List[Dict[str, str]]],
        max_tokens: int,
        engine: str,
        stop_token: str,
        temperature: float,
        top_p: float = 1,
        num_completions: int = 1,
        system_message: Optional[str] = None,
    ) :
        """Calls the Chat API.

        if the num_completions is > 2, we call the API multiple times. This is to prevent
        overflow issues that can occur when the number of completions is too large.
        """
        system_message = (
            system_message or "You are ChatGPT, a large language model trained by OpenAI."
        )

        if isinstance(prompt, str):
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
        elif isinstance(prompt, list):
            messages = prompt
            if system_message:
                messages.insert(0, {"role": "system", "content": system_message})
        else:
            raise ValueError(
                "Invalid prompt type. Prompt should be a string or a list of messages."
            )

        if num_completions > 2:
            response_combined = dict()
            num_completions_remaining = num_completions
            for i in range(0, num_completions, 2):
                # note that we are calling the same function --- this prevents backoff from being reset for the entire function
                response = DeepseekAPIWrapper.call(
                    prompt=prompt,
                    max_tokens=max_tokens,
                    engine=engine,
                    stop_token=stop_token,
                    temperature=temperature,
                    top_p=top_p,
                    num_completions=min(num_completions_remaining, 2),
                )
                num_completions_remaining -= 2
                if i == 0:
                    response_combined = response
                else:
                    response_combined.choices += response.choices
            return response_combined
        response = Client.chat.completions.create(
            model=engine,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stop=[stop_token] if stop_token else None,
            # logprobs=3,
            n=num_completions,
        )
        return response

    @staticmethod
    def get_first_response(response):
        """Returns the first response from the list of responses."""
        text = response.choices[0].message.content
        return text




class OpenaiAPIWrapper:
    @staticmethod
    def get_api_wrapper(engine: str) :
        return DeepseekAPIWrapper

    @staticmethod
    def call(
        prompt: str,
        max_tokens: int,
        engine: str,
        stop_token: str,
        temperature: float,
        num_completions: int = 1,
        **kwargs,
    ) :
        api_wrapper = OpenaiAPIWrapper.get_api_wrapper(engine)
        return api_wrapper.call(
            prompt=prompt,
            max_tokens=max_tokens,
            engine=engine,
            stop_token=stop_token,
            temperature=temperature,
            num_completions=num_completions,
            **kwargs,
        )

    @staticmethod
    def get_first_response(response) :
        api_wrapper = OpenaiAPIWrapper.get_api_wrapper(response.model)
        return api_wrapper.get_first_response(response)


def test_completion():
    prompt = 'Optimize the following Python code:\n\n# Start of code\n\nimport sys\n\nimport numpy as np\n\nn,m = [int(x) for x in sys.stdin.readline().split()]\n\nr = np.zeros(n)\n\nfor i in range(m):\n\n\ta, b = [int(x) for x in sys.stdin.readline().split()]\n\n\tr[a-1] += 1\n\n\tr[b-1] += 1\n\nfor i in range(n):\n\n\tprint((int(r[i])))\n\n# End of code\nRewrite the above Python code only from "Start of code" to "End of code", to make it more efficient WITHOUT CHANGING ITS RESULTS. Assume the code has already executed all the imports; do NOT include them in the optimized code.\n\nUse native libraries if that would make it faster than pure Python.\n\nYour output should only consist of valid Python code. Output the resulting Python with brief explanations only included as comments prefaced with #. Include a detailed explanatory comment before the code, starting with the text "# Proposed optimization:". Make the code as clear and simple as possible, while also making it as fast and memory-efficient as possible. Use vectorized operations whenever it would substantially increase performance, and quantify the speedup in terms of orders of magnitude. Eliminate as many for loops, while loops, and list or dict comprehensions as possible, replacing them with vectorized equivalents. If the performance is not likely to increase, leave the code unchanged. Fix any errors in the optimized code.'
    engine = "deepseek-r1"
    num_completions = 3
    max_tokens = 300
    response = OpenaiAPIWrapper.call(
        prompt=prompt,
        max_tokens=max_tokens,
        engine=engine,
        stop_token="Optimize the following Python code:\n\n",
        temperature=0.7,
        num_completions=num_completions,
    )
    print(OpenaiAPIWrapper.get_first_response(response))


def test_chat():
    prompt = 'Optimize the following Python code:\n\n# Start of code\n\nimport sys\n\nimport numpy as np\n\nn,m = [int(x) for x in sys.stdin.readline().split()]\n\nr = np.zeros(n)\n\nfor i in range(m):\n\n\ta, b = [int(x) for x in sys.stdin.readline().split()]\n\n\tr[a-1] += 1\n\n\tr[b-1] += 1\n\nfor i in range(n):\n\n\tprint((int(r[i])))\n\n# End of code\nRewrite the above Python code only from "Start of code" to "End of code", to make it more efficient WITHOUT CHANGING ITS RESULTS. Assume the code has already executed all the imports; do NOT include them in the optimized code.\n\nUse native libraries if that would make it faster than pure Python.\n\nYour output should only consist of valid Python code. Output the resulting Python with brief explanations only included as comments prefaced with #. Include a detailed explanatory comment before the code, starting with the text "# Proposed optimization:". Make the code as clear and simple as possible, while also making it as fast and memory-efficient as possible. Use vectorized operations whenever it would substantially increase performance, and quantify the speedup in terms of orders of magnitude. Eliminate as many for loops, while loops, and list or dict comprehensions as possible, replacing them with vectorized equivalents. If the performance is not likely to increase, leave the code unchanged. Fix any errors in the optimized code.'
    engine = "deepseek-r1"
    num_completions = 3
    max_tokens = 300
    response = OpenaiAPIWrapper.call(
        prompt=prompt,
        max_tokens=max_tokens,
        engine=engine,
        stop_token="End of code",
        temperature=0.7,
        num_completions=num_completions,
    )
    print(OpenaiAPIWrapper.get_first_response(response))



def test_basic_chat():
    prompt = "What is the capital of France?"
    engine = "deepseek-r1"
    max_tokens = 10
    response = OpenaiAPIWrapper.call(
        prompt=prompt,
        max_tokens=max_tokens,
        engine=engine,
        temperature=0.7,
        stop_token=None,
        num_completions=1,
    )
    print(OpenaiAPIWrapper.get_first_response(response))


def test_chat_with_system_message():
    prompt = "What is the capital of France?"
    engine = "deepseek-r1"
    max_tokens = 10
    system_message = "You are ChatGPT, a large language model trained by OpenAI."
    response = OpenaiAPIWrapper.call(
        prompt=prompt,
        max_tokens=max_tokens,
        engine=engine,
        stop_token=None,
        temperature=0.7,
        num_completions=1,
        system_message=system_message,
    )
    print(OpenaiAPIWrapper.get_first_response(response))


def test_chat_with_multiple_completions():
    prompt = "What is the capital of France?"
    engine = "deepseek-r1"
    max_tokens = 10
    response = OpenaiAPIWrapper.call(
        prompt=prompt,
        max_tokens=max_tokens,
        engine=engine,
        stop_token=None,
        temperature=0.7,
        num_completions=3,
    )
    print(OpenaiAPIWrapper.get_first_response(response))


def test_chat_with_message_list():
    messages = [
        {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI."},
        {"role": "user", "content": "What is the capital of France?"},
    ]
    engine = "deepseek-r1"
    max_tokens = 10
    response = OpenaiAPIWrapper.call(
        prompt=messages,
        max_tokens=max_tokens,
        engine=engine,
        stop_token=None,
        temperature=0.7,
        num_completions=1,
    )
    print(OpenaiAPIWrapper.get_first_response(response))


if __name__ == "__main__":
    print("Testing basic chat")
    test_basic_chat()

    print("Testing chat with system message")
    test_chat_with_system_message()

    print("Testing chat with multiple completions")
    test_chat_with_multiple_completions()

    print("Testing chat with message list")
    test_chat_with_message_list()

    # test the API
    print("Testing completion API")
    test_completion()
    print("Testing chat API")
    test_chat()
    


