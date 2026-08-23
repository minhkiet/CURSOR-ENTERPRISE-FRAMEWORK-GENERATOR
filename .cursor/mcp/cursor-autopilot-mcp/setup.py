from setuptools import setup, find_packages

setup(
    name="cursor-autopilot-mcp",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        line.strip()
        for line in open("requirements.txt")
        if line.strip() and not line.startswith("#") and not line.startswith("-r")
    ],
    python_requires=">=3.10",
)
