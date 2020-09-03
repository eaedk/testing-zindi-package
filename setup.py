import setuptools, sys

subprocess.check_call([sys.executable, '-mr', 'pip', 'install', 'requirements.txt'])

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zindi", # Replace with your own username
    version="0.0.1-beta",
    author="Example Author",
    author_email="user@zindi.africa",
    description="Zindi user-friendly package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=["tdqm", "requests", "pandas", "getpass"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
