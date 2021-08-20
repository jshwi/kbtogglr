"""
test._test
==========
"""
from pathlib import Path
from typing import Any

# noinspection PyPackageRequirements
import pytest

import kbtogglr

KBTOGGLR_RUN = "kbtogglr._run"
XINPUT_LIST = """
⎡ Virtual core pointer                    	id=2	[master pointer  (3)]
⎜   ↳ Virtual core XTEST pointer              	id=4	[slave  pointer  (2)]
⎜   ↳ ELAN2097:00 04F3:274F                   	id=15	[slave  pointer  (2)]
⎜   ↳ DELL090C:00 06CB:CCA6 Mouse             	id=17	[slave  pointer  (2)]
⎜   ↳ DELL090C:00 06CB:CCA6 Touchpad          	id=18	[slave  pointer  (2)]
⎜   ↳ PS/2 Synaptics TouchPad                 	id=21	[slave  pointer  (2)]
⎜   ↳ Ducky Ducky One2 SF RGB                 	id=13	[slave  pointer  (2)]
⎜   ↳ MX Master 2S Mouse                      	id=24	[slave  pointer  (2)]
⎣ Virtual core keyboard                   	id=3	[master keyboard (2)]
    ↳ Virtual core XTEST keyboard             	id=5	[slave  keyboard (3)]
    ↳ Power Button                            	id=6	[slave  keyboard (3)]
    ↳ Video Bus                               	id=7	[slave  keyboard (3)]
    ↳ Power Button                            	id=8	[slave  keyboard (3)]
    ↳ Sleep Button                            	id=9	[slave  keyboard (3)]
    ↳ Integrated_Webcam_HD: Integrate         	id=14	[slave  keyboard (3)]
    ↳ ELAN2097:00 04F3:274F Stylus            	id=16	[slave  keyboard (3)]
    ↳ Dell WMI hotkeys                        	id=19	[slave  keyboard (3)]
    ↳ DELL Wireless hotkeys                   	id=22	[slave  keyboard (3)]
    ↳ Ducky Ducky One2 SF RGB                 	id=10	[slave  keyboard (3)]
    ↳ Ducky Ducky One2 SF RGB                 	id=11	[slave  keyboard (3)]
    ↳ Ducky Ducky One2 SF RGB                 	id=12	[slave  keyboard (3)]
    ↳ MX Master 2S Keyboard                   	id=23	[slave  keyboard (3)]
∼ AT Translated Set 2 keyboard            	id=20	[floating slave]
"""


class _MockCompletedProcess:  # pylint: disable=too-few-public-methods
    """Mock ``CompletedProcess`` object returned from ```run`."""

    def __init__(self):
        self.stdout = None


_mock_completed_process = _MockCompletedProcess()


def test_success(tmp_path: Path, monkeypatch: Any) -> None:
    """Test toggling of keyboard on and off.

    :param tmp_path:    Create and return temporary directory.
    :param monkeypatch: Mock patch environment and attributes.
    """
    # set attrs
    # =========
    images = Path(__file__).parent.parent / "kbtogglr" / "images"
    off_icon = images / "off.png"
    on_icon = images / "on.png"
    cache_dir = tmp_path / ".cache"
    enable_expected = [
        "xinput, list",
        "xinput, reattach, 20, 3",
        f"notify-send, -i, {on_icon}, Enabling Keyboard..., Connected",
    ]
    disable_expected = [
        "xinput, list",
        "xinput, float, 20",
        f"notify-send, -i, {off_icon}, Disabling Keyboard..., Disconnected",
    ]

    _mock_completed_process.stdout = XINPUT_LIST.encode()
    called = []

    def _run(cmd, *_, **__):
        called.append(", ".join(cmd))
        return _mock_completed_process

    # patch attrs
    # ===========
    monkeypatch.setattr(KBTOGGLR_RUN, _run)
    monkeypatch.setattr(
        "kbtogglr._appdirs.user_cache_dir", lambda x: str(cache_dir / x)
    )

    # run tests
    # =========
    # test when toggling off
    kbtogglr.main()
    disable_output, called = called, []

    # test when toggling on
    kbtogglr.main()
    enable_output, called = called, []

    # run assertions
    # ==============
    assert off_icon.is_file()
    assert on_icon.is_file()
    assert disable_output == disable_expected
    assert enable_output == enable_expected


def test_failure(monkeypatch: Any) -> None:
    """Test error raised when getting IDs unsuccessful.

    :param monkeypatch: Mock patch environment and attributes.
    """
    _mock_completed_process.stdout = b"zsh: xinput: command not found..."
    monkeypatch.setattr(KBTOGGLR_RUN, lambda *_, **__: _mock_completed_process)
    with pytest.raises(RuntimeError) as err:
        kbtogglr.main()

    assert str(err.value) == "cannot detect keyboard id"


def test_command_not_found_error(monkeypatch: Any) -> None:
    """Test result when `xinput` is not installed.

    :param monkeypatch: Mock patch environment and attributes.
    """

    def _run(*_, **__):
        raise FileNotFoundError("[Errno 2] No such file or directory")

    monkeypatch.setattr(KBTOGGLR_RUN, _run)
    with pytest.raises(FileNotFoundError) as err:
        kbtogglr.main()

    assert str(err.value) == "xinput: command not found..."
