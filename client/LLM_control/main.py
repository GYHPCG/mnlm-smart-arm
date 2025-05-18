'''
Author: '破竹' '2986779260@qq.com'
Date: 2025-03-30 22:00:10
LastEditors: '破竹' '2986779260@qq.com'
LastEditTime: 2025-05-18 14:16:53
FilePath: \code\mnlm-smart-arm\test_voice.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from voice import generate_transcription, speak 
from dotenv import load_dotenv
from utils import Logger  
from openai import OpenAI
from typing import Optional, Dict, Any
from openai.types.beta import Assistant
from openai.types.beta.threads import Run
from command_send import send_commands_to_service
import time
import os
from agent import *

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

def wait_for_assistant(res) -> None:
    print(f'Assiant: {res}')

def wait_for_run(
    client: OpenAI,
    thread_id: str,
    run_id: str,
    logger: Logger,
    verbose: bool = False,
) -> Optional[str]:
    """
    Waits for the run to complete.

    Parameters:
        client (OpenAI): The OpenAI client.
        thread_id (str): The thread ID.
        run_id (str): The run ID.
        tools (Dict[str, Any]): The tools dictionary.
        logger (Logger): The logger.
        verbose (bool): If True, prints verbose output.

    Returns:
        str: The response from the run.
    """
    while True:
        # Retrieve the run status.
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id,
        )
        if run.status == "completed":
            messages = client.beta.threads.messages.list(
                thread_id=thread_id, limit=2, order="desc"
            )
            response = ""
            for message in messages:
                response += message.content[0].text.value  # type: ignore
                # print(
                #     f"{message.role.capitalize()}: {message.content[0].text.value}"  # type: ignore
                # )  # type: ignore
                break
            return response
        elif run.status == "in_progress" or run.status == "queued":
            if verbose:
                logger.info(
                    f"Run in progress: {run.required_action}, {run.status}, {run.tools if hasattr(run, 'tools') else ''}\n\n"
                )
            time.sleep(2)
        else:
            logger.error(f"Run failed: {run.status}\n\n")
            break
    return None

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

    thread = client.beta.threads.create()
                                        
    while True:
        global result_response

        if use_voice_input:
            user_input = generate_transcription(verbose=False)
            print(f"User: {user_input}")
            if user_input == "":
                continue
            result_response = get_response(user_input, use_rag)

        else:
            print("User: ", end="")
            user_input = input()
            result_response = get_response(user_input, use_rag)

        if user_input.lower() == "exit":
            break

        if not user_input and nudge_user:
            logger.warning("No input detected. Please speak clearly.")
            continue
        
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input,
        )
        if verbose:
            logger.info(f"Message created: {message}")

        # run = create_run(
        #     client=client,
        #     assistant_id=assistant.id,
        #     thread_id=thread.id,
        #     instructions=user_input,
        #     logger=logger,
        #     verbose=verbose,
        # )
        # response = wait_for_run(
        #     client=client,
        #     thread_id=thread.id,
        #     run_id=run.id,
        #     # tools=tools,
        #     logger=logger,
        #     verbose=verbose,
        # )
        wait_for_assistant(result_response)
        # get_respone(user_input)
        if use_voice_output:
            speak(text=result_response, client=client)

    cleanup(client=client, verbose=verbose, logger=logger)



if __name__ == "__main__":
    load_dotenv(override=True)
    verbose = True
    nudge_user = True
    use_voice_input =False  # Set to True to enable voice input. In docker container, it's not possible.
    use_voice_output = True  # Set to True to enable voice output. In docker container, it's not possible.
    use_dummy_robot_arm_server = False  # Set to True to use the simulation mode
    use_rag = False
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

