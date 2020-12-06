import setuptools, sys, subprocess

try:
    output = subprocess.run([sys.executable, '-m', 'pip', 'install','-r','requirements.txt'])
except:
    output = subprocess.run(['pip', 'install','-r','requirements.txt'])

try:
    with open("README.md", "r", encoding='utf8') as fh:
        long_description = fh.read()
except :
    long_description = "A user-friendly ZINDI package which allow Zindians to achieve all available tasks on ZINDI Platform using this package."

setuptools.setup(
    name="zindi", # Replace with your own username
    version="0.0.1-beta",
    author="The CIA TEAM",
    author_email="ai.team.future.coders.1@gmail.com",
    description="Zindi user-friendly package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=["tdqm", "requests", "pandas", "requests-toolbelt" ], # "getpass"
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
