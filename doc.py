#!/usr/bin/env python3

import cmd
import openai
import os
import sys

# Set up OpenAI API credentials
openai.api_key = "<TOKEN>" 

# Define a class to handle the command-line interface
class DocCLI(cmd.Cmd):
    intro = "Welcome to the DocCLI. Type 'help' to list available commands."
    prompt = "(doc) "

    def __init__(self):
        super().__init__()
        self.commands = []

    # Define the 'start' command to start recording commands
    def do_start(self, arg):
        """Start recording commands"""
        print("Recording commands...")
        self.commands = []

    # Define the 'stop' command to stop recording commands and generate documentation
    def do_stop(self, arg):
        """Stop recording commands and generate documentation"""
        print("Generating documentation...")

        # Use OpenAI API to generate documentation for each command
        doc_strings = []
        for command in self.commands:
            response = openai.Completion.create(
              engine="davinci-003",
              prompt=command + "\n\nExplain the purpose and functionality of this command:",
              max_tokens=1024,
              n=1,
              stop=None,
              temperature=0.5,
            )

            doc_strings.append(response.choices[0].text.strip())

        # Write documentation to a Markdown file
        with open("documentation.md", "w") as f:
            for i, command in enumerate(self.commands):
                f.write(f"## Command {i+1}: {command}\n\n")
                f.write(doc_strings[i] + "\n\n")

        print(f"Documentation generated and saved to {os.getcwd()}/documentation.md")

    # Define the default command to record user input
    def default(self, line):
        """Record user input"""
        self.commands.append(line)

    # Define the 'quit' command to exit the application
    def do_quit(self, arg):
        """Exit the DocCLI"""
        print("Goodbye!")
        return True

if __name__ == "__main__":
    DocCLI().cmdloop()

