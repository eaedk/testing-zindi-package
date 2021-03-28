import setuptools


short_description = "A user-friendly Zindi package which allows Zindians to\
 get things done on the ZINDI Platform."

with open("README.md") as fh:
    long_description = fh.read()


setuptools.setup(
    name="zindi",
    version="0.0.1",
    author="The CIA TEAM",
    author_email="ai.team.future.coders.1@gmail.com",
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eaedk/testing-zindi-package",
    packages=["zindi"],
    install_requires=["tdqm", "requests", "pandas", "requests-toolbelt" ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
)
