# import os
# from typing import Dict, Any, List, Optional, Union
import openai 
# import random
# import time
# import json
# from wrapper import BaseAPIWrapper
# from collections import Counter


# class DeepseekAPIWrapper(BaseAPIWrapper):
#     @staticmethod
#     def call(
#         prompt: Union[str, List[Dict[str, str]]],
#         max_tokens: int,
#         engine: str,
#         stop_token: str,
#         temperature: float,
#         top_p: float = 1,
#         num_completions: int = 1,
#         system_message: Optional[str] = None,
#     ) -> dict:
#         """Calls the Chat API.

#         if the num_completions is > 2, we call the API multiple times. This is to prevent
#         overflow issues that can occur when the number of completions is too large.
#         """
#         system_message = (
#             system_message or "You are ChatGPT, a large language model trained by OpenAI."
#         )

#         if isinstance(prompt, str):
#             messages = []
#             if system_message:
#                 messages.append({"role": "system", "content": system_message})
#             messages.append({"role": "user", "content": prompt})
#         elif isinstance(prompt, list):
#             messages = prompt
#             if system_message:
#                 messages.insert(0, {"role": "system", "content": system_message})
#         else:
#             raise ValueError(
#                 "Invalid prompt type. Prompt should be a string or a list of messages."
#             )

#         if num_completions > 2:
#             response_combined = dict()
#             num_completions_remaining = num_completions
#             for i in range(0, num_completions, 2):
#                 # note that we are calling the same function --- this prevents backoff from being reset for the entire function
#                 response = DeepseekAPIWrapper.call(
#                     prompt=prompt,
#                     max_tokens=max_tokens,
#                     engine=engine,
#                     stop_token=stop_token,
#                     temperature=temperature,
#                     top_p=top_p,
#                     num_completions=min(num_completions_remaining, 2),
#                 )
#                 num_completions_remaining -= 2
#                 if i == 0:
#                     response_combined = response
#                 else:
#                     response_combined["choices"] += response["choices"]
#             return response_combined
#         response = openai.ChatCompletion.create(
#             model=engine,
#             messages=messages,
#             temperature=temperature,
#             max_tokens=max_tokens,
#             top_p=top_p,
#             stop=[stop_token] if stop_token else None,
#             # logprobs=3,
#             n=num_completions,
#         )

#         return response

#     @staticmethod
#     def get_first_response(response) -> Dict[str, Any]:
#         """Returns the first response from the list of responses."""
#         text = response["choices"][0]["message"]["content"]
#         return text

#     @staticmethod
#     def get_majority_answer(response) -> Dict[str, Any]:
#         """Returns the majority answer from the list of responses."""
#         answers = [choice["message"]["content"] for choice in response["choices"]]
#         answers = Counter(answers)
#         # if there is a tie, return the first answer
#         if len(answers) == 1:
#             return answers.most_common(1)[0][0]

#         if answers.most_common(1)[0][1] == answers.most_common(2)[1][1]:
#             return DeepseekAPIWrapper.get_first_response(response)

#         return answers.most_common(1)[0][0]

#     @staticmethod
#     def get_all_responses(response) -> Dict[str, Any]:
#         """Returns the list of responses."""
#         # return [choice["message"]["content"] for choice in response["choices"]]  # type: ignore
#         return [
#             {"generated_answer": choice["message"]["content"], "logprobs": None}
#             for choice in response["choices"]
#         ]
    
# def test():
#     wrapper = DeepseekAPIWrapper()

#     response = wrapper.call(
#         prompt="The quick brown fox",
#         max_tokens=10,
#         engine="deepseek-r1",
#         stop_token="\n",
#         temperature=0.7,
#     )

#     print(response)

if __name__ == "__main__":
    # test()
    openai.base_url="http://503804.proxy.nscc-gz.cn:8888/v1/"
    openai.api_key="token-YatCC2025"
    messages = []
    messages.append({"role": "system", "content": "You are an AI assistant."})
    messages.append({"role": "user", "content": "What is the capital of China?"})
    response = openai.Completion.create(
        model="deepseek-r1",
        messages=messages,
        temperature=0.7,
        max_tokens=100,
        top_p=1,
        stop=["\n"],
        n=1,
    )
    print(response)