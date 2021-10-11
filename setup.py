from setuptools import setup
setup(
    install_requires=["streamlit"],
    entry_points={"console_scripts": ["clista=clista:main"]},
)
