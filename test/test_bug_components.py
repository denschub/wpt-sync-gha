import os
from sync import bugcomponents


def test_remove(config, directory):
    wpt_root = directory(config["gecko"]["path"]["wpt"])

    # Create some sample files
    for path in ["../1.html", "a/1.html", "b/1.html", "c/d/1.html"]:
        path = os.path.join(wpt_root, path)
        try:
            os.makedirs(os.path.dirname(path))
        except OSError:
            pass
        with open(path, "w") as f:
            f.write("test")

    moz_build_path = os.path.join(wpt_root,
                                  os.pardir,
                                  "moz.build")

    initial = """
# -*- Mode: python; indent-tabs-mode: nil; tab-width: 40 -*-
# vim: set filetype=python:

WEB_PLATFORM_TESTS_MANIFESTS += [
    ('meta/MANIFEST.json', 'tests/'),
    ('mozilla/meta/MANIFEST.json', 'mozilla/tests/')
]

with Files("tests/a/**"):
    BUG_COMPONENT = ("Testing", "web-platform-tests")

with Files("tests/b/**"):
    BUG_COMPONENT = ("Testing", "web-platform-tests")

with Files("tests/c/**"):
    BUG_COMPONENT = ("Testing", "web-platform-tests")

with Files("tests/c/e/**"):
    BUG_COMPONENT = ("Testing", "web-platform-tests")

with Files("tests/f/**"):
    BUG_COMPONENT = ("Testing", "web-platform-tests")

with Files("1*"):
    BUG_COMPONENT = ("Testing", "web-platform-tests")
"""

    expected = """
# -*- Mode: python; indent-tabs-mode: nil; tab-width: 40 -*-
# vim: set filetype=python:

WEB_PLATFORM_TESTS_MANIFESTS += [
    ('meta/MANIFEST.json', 'tests/'),
    ('mozilla/meta/MANIFEST.json', 'mozilla/tests/')
]

with Files("tests/a/**"):
    BUG_COMPONENT = ("Testing", "web-platform-tests")

with Files("tests/b/**"):
    BUG_COMPONENT = ("Testing", "web-platform-tests")

with Files("tests/c/**"):
    BUG_COMPONENT = ("Testing", "web-platform-tests")

with Files("1*"):
    BUG_COMPONENT = ("Testing", "web-platform-tests")
"""

    with open(moz_build_path, "w") as f:
        f.write(initial)

    assert bugcomponents.remove_obsolete(moz_build_path) == expected
