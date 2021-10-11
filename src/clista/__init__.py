import argparse
import sys

__version__ = (0, 0, 2)
__version_str__ = ".".join(str(i) for i in __version__)


def main():
    # write st app dynamically or gen code?
    # use template or AST?
    argp = argparse.ArgumentParser()
    argp.add_argument(
        "--sample",
        action="store_true",
        help="Generate sample program from `hey` CLI tool",
    )
    args = argp.parse_args()
    if args.sample:
        import clista.hey_help as hey_help

        generate_streamlit_app(hey_help.text.strip())
    else:
        generate_streamlit_app(sys.stdin.read().strip())


def generate_streamlit_app(cli_help, appfile="stapp.py"):
    STREAMLIT_APP = """
import subprocess
import streamlit as st
opts = []
"""
    stapp = [STREAMLIT_APP]

    lines = [i for i in cli_help.splitlines() if i.strip()]

    # parse to get the command, the required arg
    # Usage: hey [options...] <url>
    usage_msg = lines[0]
    _usage, name, *_, cmd_arg = usage_msg.split()

    stapp.append(f"st.title(f'{name} webapp')")
    stapp.append(f"st.caption('*Made with CLISTA v{__version_str__}*')")
    stapp.append(f"cmd_arg = st.text_input(f'{cmd_arg}')")

    options = [i.strip() for i in lines[1:] if i.strip().startswith("-")]
    opt_msg = {}
    for line in options:
        opt, msg = line.split(maxsplit=1)
        opt_msg[opt.strip("-")] = line.strip()
        opt_var = opt.strip("-").replace("-", "_")

        stapp.append(f"opt_{opt_var} = st.text_input('{line.strip()}')")
        stapp.append(f"opts.append(('{opt}', opt_{opt_var}))")

    APP_END = """
run =st.button("run")
opts = sum([[o, v] for (o, v) in opts if v], start=[])
if run:
    name = "%s"
    cmd = [name, *opts, cmd_arg]
    st.write(f"Running {cmd}")
    p = subprocess.run(cmd, check=True, capture_output=True)
    st.markdown("```\\n" + p.stdout.decode("utf-8") + "\\n```")
"""

    end = APP_END % (name)
    with open(appfile, "wt") as f:
        f.write("\n".join(stapp + end.splitlines()))
        print(
            "Wrote stapp.py, please copy and edit as needed then run streamlit run stapp.py"
        )
        print("NOTE: rerun would overwrite stapp.py")

    # run the app via streamlit when option passed
