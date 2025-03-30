'''
Author: '破竹' '2986779260@qq.com'
Date: 2025-03-30 22:00:10
LastEditors: '破竹' '2986779260@qq.com'
LastEditTime: 2025-03-30 22:46:19
FilePath: \code\mnlm-smart-arm\test_voice.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from voice import generate_transcription, speak 
from dotenv import load_dotenv
from utils import Logger  
from openai import OpenAI
from typing import Optional, Dict
from openai.types.beta import Assistant
from openai.types.beta.threads import Run
def create_assistant(
    client: OpenAI,logger: Logger, verbose: bool = False
) -> Assistant:
    """Create a GPT based orchestration assistant.

    Parameters:
        client (OpenAI): The OpenAI client.
        tools (Dict[str, Tool]): The tools dictionary.
        logger (Logger): The logger.
        verbose (bool): If True, prints verbose output.

    Returns:
        Assistant: The assistant.
    """
    if not client:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
   
    assistant = client.beta.assistants.create(
        name="Voice Robot Controller",
        instructions="""
            You have a brain and a robot arm, and you receive voice command from the human being, and respond accordingly.
        """,
        model="gpt-3.5-turbo-1106",
    )
    if verbose:
        logger.info(f"Assistant created: {assistant}")
    return assistant
def cleanup(
    client: OpenAI, logger: Optional[Logger] = None, verbose: bool = False
) -> None:
    pass

def create_run(
    client: OpenAI,
    assistant_id: str,
    thread_id: str,
    instructions: str,
    logger: Logger,
    verbose: bool,
) -> Run:
    """Creates a run for the assistant.

    Parameters:
        client (OpenAI): The OpenAI client.
        assistant_id (str): The assistant ID.
        thread_id (str): The thread ID.
        instructions (str): The instructions.
        logger (Logger): The logger.
        verbose (bool): If True, prints verbose output.

    Returns:
        Run: The run.
    """
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions=instructions,
    )
    if verbose:
        logger.info(f"Run created: {run}")
    return run


def start_conversation(
    verbose: bool,
    logger: Logger,
    nudge_user: bool,
    use_voice_input: bool,
    use_voice_output: bool,
    use_dummy_robot_arm_server: bool,
    use_rag: bool,
) -> None:
    client = OpenAI()

    assistant = create_assistant(
        client=client, logger=logger, verbose=verbose
    )
    
    while True:
        if use_voice_input:
            user_input = generate_transcription(verbose=False)
            print(f"User: {user_input}")
        else:
            print("User: ", end="")
            user_input = input()

        if user_input.lower() == "exit":
            break

        if not user_input and nudge_user:
            logger.warning("No input detected. Please speak clearly.")
            continue

        if use_voice_output:
            speak(text=user_input, client=client)

    cleanup(client=client, verbose=verbose, logger=logger)



if __name__ == "__main__":
    load_dotenv(override=True)
    verbose = True
    nudge_user = True
    use_voice_input = True  # Set to True to enable voice input. In docker container, it's not possible.
    use_voice_output = True  # Set to True to enable voice output. In docker container, it's not possible.
    use_dummy_robot_arm_server = True  # Set to True to use the simulation mode
    use_rag = True
    logger = Logger(__name__)
    start_conversation(
        verbose=verbose,
        nudge_user=nudge_user,
        use_voice_input=use_voice_input,
        use_voice_output=use_voice_output,
        use_dummy_robot_arm_server=use_dummy_robot_arm_server,
        use_rag=use_rag,
        logger=logger,
    )

