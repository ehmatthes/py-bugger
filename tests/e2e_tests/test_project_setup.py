"""Test aspects of project setup that might interfere with CI and the release process."""


def test_editable_requirement(e2e_config):
    """Make sure there's no editable entry for py-bugger in requirements.txt.

    This entry gets inserted when running pip freeze, from an editable install.
    """
    path_req_txt = e2e_config.path_root / "requirements.txt"

    contents = path_req_txt.read_text()
    assert "-e file:" not in contents
