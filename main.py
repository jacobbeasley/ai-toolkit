import typer as typer
from typing_extensions import Annotated

import config
import openaiapp
from config import getconfig, updateconfig
import os
import yaml
import json
from functions import readfile

# bootstrap typer
app = typer.Typer(no_args_is_help=True)
app.add_typer(openaiapp.app, name="openai")

#ui_thread = None
@app.command(help="Start Web UI")
def start(
        port: Annotated[str, typer.Option(help="Port number")] = getconfig("SERVER_PORT"),
        share: Annotated[bool, typer.Option(help="Share Public URL")] = False,
        inbrowser: Annotated[bool, typer.Option(help="Open Web Browser")] = False,
):
    startapp(inbrowser, port, share)

def startapp(inbrowser, port, share):
    import gradio as gr
    with gr.Blocks() as appuiblocks:
        # Generate Novel
        with gr.Tabs():
            # Apps Tab
            apps_dir = os.path.join(getconfig("AI_TEMPLATES_DIR"), "apps")
            app_names = [d for d in os.listdir(apps_dir) if os.path.isdir(os.path.join(apps_dir, d))]
            
            if len(app_names) > 0 or False:
                with gr.Tab("Apps"):
                    with gr.Tabs():
                        for app_name in app_names:
                            app_path = os.path.join(apps_dir, app_name)
                            manifest_path = os.path.join(app_path, "manifest.yaml")
                            manifest = yaml.safe_load(readfile(manifest_path))
                            app_description = manifest.get("description", app_name)

                            def app_fn(*args):
                                return openaiapp.call(
                                    request=json.dumps({inp["name"]: val for inp, val in zip(manifest.get("inputs", []), args)}), 
                                    template=os.path.join("apps", app_name, "template"), 
                                    stop_at_section_block=manifest.get("stop_characters", None)
                                )
                            with gr.Tab(manifest.get("name", app_name)):
                                def inp_to_gradio(inp):
                                    if inp["type"] == "text":
                                        return gr.Textbox(label=inp.get("label", inp["name"]), lines=4, value="")
                                    elif inp["type"] == "number":
                                        return gr.Number(label=inp.get("label", inp["name"]), value=0)
                                    elif inp["type"] == "select":
                                        return gr.Dropdown(label=inp.get("label", inp["name"]), choices=inp.get("choices", []), value=inp.get("default", None))
                                    elif inp["type"] == "checkbox":
                                        return gr.Checkbox(label=inp.get("label", inp["name"]), value=inp.get("default", False))
                                    elif inp["type"] == "textarea":
                                        return gr.Textbox(label=inp.get("label", inp["name"]), lines=8, value="")
                                    elif inp["type"] == "image":
                                        return gr.Image(label=inp.get("label", inp["name"]), type="filepath")
                                    elif inp["type"] == "audio":
                                        return gr.Audio(label=inp.get("label", inp["name"]), type="filepath")
                                    elif inp["type"] == "markdown":
                                        return gr.Markdown(label=inp.get("label", inp["name"]), value="")
                                    elif inp["type"] == "html":
                                        return gr.HTML(label=inp.get("label", inp["name"]), value="")
                                    elif inp["type"] == "color":
                                        return gr.ColorPicker(label=inp.get("label", inp["name"]), value=inp.get("default", "#FFFFFF"))
                                    elif inp["type"] == "date":
                                        return gr.Date(label=inp.get("label", inp["name"]), value=inp.get("default", "2023-01-01"))
                                    elif inp["type"] == "datetime":
                                        return gr.DateTime(label=inp.get("label", inp["name"]), value=inp.get("default", "2023-01-01T00:00:00"))
                                    else:
                                        raise ValueError(f"Unsupported input type: {inp['type']}")
                                
                                gr.Interface(
                                    fn=app_fn,
                                    inputs=[inp_to_gradio(inp) for inp in manifest.get("inputs", []) if inp["type"] == "text"],
                                    outputs=gr.Textbox(label="Output"),
                                    description=app_description,
                                    title=manifest.get("name", app_name)
                                ) 

            # Config
            with gr.Tab("Config"):
                with gr.Tabs():
                    with gr.Tab("Config"):
                        def config_submit(c):
                            updateconfig(c)
                            return "Saved. Note that changing server port will not work. "
                        gr.Interface(fn=config_submit, outputs="textbox",
                                     inputs=gr.Matrix(
                                         headers=["Key", "Value"],
                                         datatype=["str", "str"],
                                         row_count=len(config.getallconfig()),
                                         label="Config Options",
                                         value=[(k, v) for k, v in config.getallconfig().items()]
                                     ))
                    with gr.Tab("Test"):
                        gr.Interface(
                            fn=openaiapp.call, inputs=[
                                gr.Textbox(label="Request (JSON if using template that requires multiple fields)",
                                           value="What is your name?"),
                                gr.Textbox(label="Template Name", value="")
                            ],
                            outputs="textbox",
                            api_name="test_llm")
    # Launch app!
    appuiblocks.launch(server_port=int(port), show_error=True, share=share, inbrowser=inbrowser, show_api=True)

if __name__ == "__main__":
    app()

