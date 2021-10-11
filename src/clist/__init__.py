STREAMLIT_APP = """
import subprocess
import streamlit as st
"""
def main():
    print("CLIST")
    # write st app dynamically or gen code?
    # use template or AST?

    stapp = [STREAMLIT_APP]

    # get help msg of the command
    with open("heyhelp.txt") as f:
        lines = [i for i in f.readlines() if i.strip()]

    # parse to get the command, the required arg
    # Usage: hey [options...] <url>
    usage_msg = lines[0]
    _usage, name, *_, cmd_arg = usage_msg.split()

    stapp.append(f"st.title(f'{name} webapp')")
    stapp.append(f"cmd_arg = st.text_input(f'{cmd_arg}')")

    options = [i.strip() for i in lines[1:] if i.strip().startswith("-")]
    opt_msg = {}
    for line in options:
        opt, msg = line.split(maxsplit=1)
        opt_msg[opt.strip("-")] = line.strip()

        stapp.append(f"x = st.text_input(f'{msg.strip()}')")


    # TODO get what use input an turn to cmd args
    opts=[]

    APP_END = """
run =st.button("run")
if run:
    name = "%s"
    opts = []
    cmd = [name, *opts, cmd_arg]
    st.write(f"Running {cmd}")
    p = subprocess.run(cmd, check=True, capture_output=True)
    st.markdown("```\\n" + p.stdout.decode("utf-8") + "\\n```")
"""

    end = APP_END % (name)
    with open("stapp.py", "wt") as f:
        f.write("\n".join(stapp + end.splitlines()))
        print("Wrote stapp.py")

    # parse all options, turn to a text field

    # have a button to execute

    # convert to streamlit app.py
    # run the app via streamlit
