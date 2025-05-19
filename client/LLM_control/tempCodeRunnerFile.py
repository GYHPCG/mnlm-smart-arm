assistant = client.beta.assistants.create(
        name="Voice Robot Controller",
        instructions="""
            You have a brain and a robot arm, and you receive voice command from the human being, and respond accordingly.
        """,
        model="gpt-3.5-turbo-1106",
    )