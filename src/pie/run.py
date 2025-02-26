import pandas as pd
from tqdm import tqdm


from src.pie.task_init import PieInit
from src.pie.task_iterate import PieIterate
from src.pie.feedback import PieFeedback

from src.utils import retry_parse_fail_prone_cmd

ENGINE = "deepseek-r1"


@retry_parse_fail_prone_cmd
def iterative_pie(slow_code: str, max_attempts: int, feedback_type: str, temperature: float):

    # initialize all the required components

    # generation of the first fast version
    task_init = PieInit(engine=ENGINE, prompt_examples="data/prompt/pie/init.txt", temperature=temperature)

    iterate_prompt = "data/prompt/pie/iterate.txt"
    # getting feedback
    if feedback_type == "naive":
        task_feedback = lambda **kwargs: "It could be faster"
        iterate_prompt = "data/prompt/pie/iterate_genericfb.txt"

    elif feedback_type == "none":
        task_feedback = lambda **kwargs: ""
        iterate_prompt = "data/prompt/pie/iterate_nofb.txt"

    else:
        task_feedback = PieFeedback(engine=ENGINE, prompt_examples="data/prompt/pie/feedback.txt", temperature=temperature)

    # iteratively improving the code
    task_iterate = PieIterate(engine=ENGINE, prompt_examples=iterate_prompt, temperature=temperature)

    # Initialize the task

    n_attempts = 0

    log = []
    feedback = None

    while n_attempts < max_attempts:

        if n_attempts == 0:
            fast_code = task_init(slow_code=slow_code)
        else:
            fast_code = task_iterate(slow_code=slow_code, feedback=feedback)

        # feedback = task_feedback(slow_code=slow_code)
        feedback = task_feedback(slow_code=fast_code)

        log.append({"fast_code": fast_code, "feedback": feedback, "slow_code": slow_code, "attempt": n_attempts})
        show_example(**log[-1])

        if "this code is not slow" or "not slow" in feedback.lower():
            break

        slow_code = fast_code

        n_attempts += 1

    return log

def show_example(**kwargs):
    # shows {"fast_code": fast_code, "feedback": feedback, "slow_code": slow_code, "attempt": n_attempts}
    print(f"SLOW CODE:\n{kwargs['slow_code']}\n")
    print(f"\n\nFEEDBACK:\n{kwargs['feedback']}\n")
    print(f"\n\nFAST CODE:\n{kwargs['fast_code']}\n")
    print("-" * 100)
    
def run_over_slow_programs(slow_programs_file: str, max_attempts: int, outfile: str, feedback_type: str, temperature: float=0.7, backup_file: str = None):
    with open(slow_programs_file, 'r') as file:
        slow_programs_str = file.read()
    run_logs=iterative_pie(slow_code=slow_programs_str, max_attempts=max_attempts, feedback_type=feedback_type, temperature=temperature)
    with open(outfile, 'w') as file:
        file.write(str(run_logs[0].get('fast_code')))
    return str(run_logs[0].get('fast_code'))

def run_over_slow_code(slow_code: str, max_attempts: int,  feedback_type: str, temperature: float=0.7):
    run_logs=iterative_pie(slow_code=slow_code, max_attempts=max_attempts, feedback_type=feedback_type, temperature=temperature)
    return str(run_logs[0].get('fast_code'))

def test_f():
    run_over_slow_programs(
        slow_programs_file="data/prompt/pie/test.ll", max_attempts=3, outfile="data/prompt/pie/output.ll",feedback_type="rich", temperature=0.6
    )

def test():
    slow_code = ('''
    
    ''')
    fastcode=run_over_slow_code(slow_code=slow_code, max_attempts=3, feedback_type="rich", temperature=0.6)
    print(fastcode)

if __name__ == "__main__":
    import sys
    if sys.argv[1] == "test_f":
        test_f()
    elif sys.argv[1] == "test":
        test()
    else:
        import argparse
        import os
        args = argparse.ArgumentParser()
        args.add_argument("--slow_programs_file", type=str, required=True)
        args.add_argument("--max_attempts", type=int, default=3)
        args.add_argument("--outfile", type=str, required=True)
        args.add_argument("--feedback_type", type=str)
        args.add_argument("--temperature", type=float, default=0.0)
        args.add_argument("--backup_file", type=str)
        args = args.parse_args()
        
        run_over_slow_programs(slow_programs_file=args.slow_programs_file, max_attempts=args.max_attempts, outfile=args.outfile, feedback_type=args.feedback_type, temperature=args.temperature, backup_file=args.backup_file)
