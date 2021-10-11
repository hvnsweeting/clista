STREAMLIT_APP = """
import subprocess
import streamlit as st
"""
def main():
    print("CLIST")
    # get help msg of the command

    # parse to get the command, the required arg
    # Usage: hey [options...] <url>
    stapp = [STREAMLIT_APP]

    with open("heyhelp.txt") as f:
        lines = [i for i in f.readlines() if i.strip()]

    usage_msg = lines[0]
    _usage, name, *_, cmd_arg = usage_msg.split()

    stapp.append(f"st.title(f'{name} webapp')")
    stapp.append(f"cmd_arg = st.text_input(f'{cmd_arg}')")

    options = [i.strip() for i in lines[1:] if i.strip().startswith("-")]
    opt_msg = {}
    for line in options:
        opt, msg = line.split(maxsplit=1)
        opt_msg[opt.strip("-")] = msg.strip()

        stapp.append(f"x = st.text_input(f'{msg.strip()}')")


    stapp.append('run =st.button("run")')
    stapp.append('if not run: exit()')
    # TODO get what use input an turn to cmd args
    opts=[]
    stapp.append(f'name = "{name}"')
    stapp.append(f'opts = []')
    stapp.append(f'cmd = [name, *opts, cmd_arg]')
    stapp.append('st.write(f"Running {cmd}")')
    stapp.append('p = subprocess.run(cmd, check=True, capture_output=True)')
    stapp.append('st.markdown("```\\n" + p.stdout.decode("utf-8") + "\\n```")')
    with open("stapp.py", "wt") as f:
        f.write("\n".join(stapp))
        print("Wrote stapp.py")

    # write st app dynamically or gen code?
    # parse all options, turn to a text field

    # have a button to execute

    # convert to streamlit app.py
    # run the app via streamlit
