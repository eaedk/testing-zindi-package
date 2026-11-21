# This repository has moved

**The zindi package now lives at [eaedk/zindi-package](https://github.com/eaedk/zindi-package).**
The history of this repository, including every contribution, has been merged there.

Version 1.0 is a rewrite for Zindi's new platform (zindi.world), with a command line,
notebook widgets, and clients for Python, JavaScript, R and Rust.
Documentation: <https://zindi.readthedocs.io>.

## Install

```bash
pip install "zindi @ git+https://github.com/eaedk/zindi-package.git#subdirectory=python"
```

(`pip install zindi` once version 1.0 is on PyPI.)

## Old notebooks still work

If a notebook runs

```bash
pip install git+https://github.com/eaedk/testing-zindi-package.git
```

it now installs the maintained package, and the 0.x interface is still there:

```python
from zindi.user import Zindian
user = Zindian(username="your_username")
```

For new code, use the modern client:

```python
import zindi
client = zindi.Client()
client.competitions()
```

See the [migration guide](https://zindi.readthedocs.io/en/latest/migration/).

## Thank you

To everyone who opened issues, sent pull requests and forked this repository: your ideas
shaped version 1.0. You are credited in the new repository's
[acknowledgements](https://github.com/eaedk/zindi-package/blob/dev/ACKNOWLEDGEMENTS.md).
Please open new issues and pull requests on
[eaedk/zindi-package](https://github.com/eaedk/zindi-package/issues).
