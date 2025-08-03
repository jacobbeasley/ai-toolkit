<img src="novelai3.jpg" alt="logo" style="width:640px;"/>

# AI Toolkit

AI Toolkit is an open-source project designed to empower would-be authors prompt engineers to be able to use AI to build their own apps without writing code. Its also a starter app I plan to use for personal projects. It is not done yet. 

Note: This is mostly a hobby project of mine, so set expectations accordingly! 

## Installation

You will need Python installed. I document what version I normally use in .python-version, but I think 3.10.x and newer should work. 

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/novelai.git
   cd novelai
   ```
   Optional: Setup a [python virtual environment](https://docs.python.org/3/library/venv.html)
2. Install dependencies: (note: you can sometimes just double click on install.sh or install.bat)
   ```bash
   pip install -r requirements.txt
   ```
   Optional: Install additional dependencies to generate audiobooks (python packages for respective models and ffmpeg for Mac/Windows/Linux)
   ```bash
   pip install -r requirements.kokoro.txt
   pip install -r requirements.coqui.txt
   pip install -r requirements.llasa3b.txt
   pip install -r requirements.sparktts.txt
   brew install ffmpeg
   # cuda support for nvidia cards:
   pip uninstall torch torchaudio
   pip install torch==2.5.1+cu124 torchaudio==2.5.1+cu124 --index-url https://download.pytorch.org/whl/cu124
   ```
3. Configure Large Language Model: 
   - By default, it expects you have [LM Studio installed](https://lmstudio.ai/) and [running a server](https://lmstudio.ai/docs/api/server) locally running the lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF model. 
   - If this is not the case, such as if you want to use a different model or are using OpenAI's ChatGPT, then edit the configuration in novelai.bat and novelai.sh.
   - You can also enable debug logs by modifying novelai.bat and novelai.sh (based on if you are using windows or mac/linux). 
4. Run the application using novelai.bat or novelai.sh. It will open your web browser automatically. 
   ```bash
   ./novelai.sh
   ```
   ```cmd
   novelai.bat
   ```

## Advanced Usage

1. **Customize Templates**
   - You can modify the templates in templates/ to change the behavior when generating outlines
   - You can also set the AI_TEMPLATES_DIR environment variable to provide different directories of templates. 
2. **Command Line Interface**
   - a rich and expressive command line interface is available should you choose to use it to automate common tasks.
   ```bash
   ./novelai.sh --help

   Usage: main.py [OPTIONS] COMMAND [ARGS]...
   
   ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
   │ --install-completion          Install completion for the current shell.                                              │
   │ --show-completion             Show completion for the current shell, to copy it or customize the installation.       │
   │ --help                        Show this message and exit.                                                            │
   ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
   ╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────╮
   │ start      Start Web UI                                                                                              │
   │ openai                                                                                                               │
   ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
   ```
5. **Functions Library**
   - I've created a number of useful utility functions that you can use for other projects in functions.py
   - I also created an expressive language for building and executing chains of LLM prompts using *just simple jinja2 templates*. For a powerful example, see templates/alt/noveloutline.jinja2.
   - If you are interested in the prompts, it is worth reviewing my approach to getting structured JSON back from any large language model. I have it automatically pass invalid JSON back to the LLM to be corrected (and it works!). 
   - This could easily be used as a starter project for other projects. The command line parameters all use typer and the web user interface uses Gradio. Jinja2 and OpenAI are used to communicate with the large language models. TTS and ffmpeg for audio generation and merging.
   - The command line tools for audiobook generation or making open api calls could be used stand-alone in their own right. They are much simpler that other tools (but also less powerful and slower). 

## AI Techniques and Technologies Used

1. **Prompt Engineering**: I use a number of prompt engineering techniques with the open source [openai libraries](https://platform.openai.com/docs/libraries)
2. **Highly Tuned Prompts**: In many cases, I have had to iterate and tune the prompts to get the desired outcome. I have targeted small language models (7B params) when testing to ensure a wide level of compatibility (what works with small will work better with large!). 
3. **Chain of Thought**: You will note that in the example JSON that I use when generating a novel outline, I actually include extra fields that I never actually use (such as act_list) simply because this prompts the AI to think through details in a certain order. I also in some cases (ex: templates/alt/noveloutline.jinja2) perform a chain of prompts assembling data in one step and then using it in later steps systematically to get the desired result.
4. **N-Shot**: In some cases, I provide multiple examples (see templates/generatechapter.jinja2) to help it to pick up on style and formatting. 
5. **Formatted Responses**: I prompt the LLM to output as JSON providing samples (at times leveraging N-Shot) to get it to output in JSON. Note also that I already start its repsonse with "```json" in many cases so that it will respond with JSON and close the response with tick marks so that I know that it is done and stop receiving more characters.
6. **Text to Speech**: I am using the [TTS library](https://github.com/coqui-ai/TTS) by coqui-ai as well as (by default) its [XTTS-V2](https://huggingface.co/coqui/XTTS-v2) model which seems to provide excellent results. Note that it is unclear what its licensing model will be since coqui seems to have shut down (though its model and tools will live in, I hope). I then leverage [ffmpeg](https://ffmpeg.org/)
7. **Automatic JSON clenaup**: I am using the LLM to clean up JSON if it sends back JSON that is invalid. 

## Contributing

We welcome contributions from the community! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed explanation of your changes.

## License

This project is licensed under the [Apache License Version 2.0](LICENSE).

## Acknowledgments

Special thanks to the open-source community and all contributors who make this project possible and to the project founder and maintainer [Jacob Beasley](https://www.linkedin.com/in/jacobbeasley/).

---

Ready to create your next masterpiece? Dive into NovelAI and let your creativity flow!
