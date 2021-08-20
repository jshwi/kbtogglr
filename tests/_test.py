"""
test._test
==========
"""
from pathlib import Path
from typing import Any, Tuple

# noinspection PyPackageRequirements
import pytest

import kbtogglr

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


class MockContext:
    """Base class for simple ``with`` statements."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Nothing to do."""

    def __enter__(self) -> Any:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Nothing to do."""


class MockPopenXinputList(  # pylint: disable=too-few-public-methods
    MockContext
):
    """Patch successful command."""

    # noinspection PyMethodMayBeStatic
    def communicate(self) -> Tuple[str, str]:  # pylint: disable=no-self-use
        """Patch communicate to return ``xinput list``.

        :return: Tuple of patched stdout and stderr.
        """
        return XINPUT_LIST, ""


class MockPopenCommandNotFound(  # pylint: disable=too-few-public-methods
    MockContext
):
    """Patch failed command."""

    # noinspection PyMethodMayBeStatic
    def communicate(self) -> Tuple[str, str]:  # pylint: disable=no-self-use
        """Patch communicate to notify command not found.

        :return: Tuple of patched stdout and stderr.
        """
        return "zsh: xinput: command not found...", ""


def main(capsys: Any) -> str:
    """Run the package's main function and return its output.

    :param capsys:  Capture sys stdout and stderr.
    :return:        Stripped capsys stdout result.
    """
    kbtogglr.main()
    output = capsys.readouterr()
    return output.out.strip()


def test_success(tmp_path: Path, monkeypatch: Any, capsys: Any) -> None:
    """Test toggling of keyboard on and off.

    :param tmp_path:    Create and return temporary directory.
    :param monkeypatch: Mock patch environment and attributes.
    :param capsys:      Capture sys stdout and stderr.
    """
    # set attrs
    # =========
    images = Path(__file__).parent.parent / "kbtogglr" / "images"
    off_icon = images / "off.png"
    on_icon = images / "on.png"
    cache_dir = tmp_path / ".cache"
    enable_expected = (
        f"notify-send, -i, {on_icon}, Enabling Keyboard..., Connected\n"
        "xinput, reattach, 20, 3"
    )
    disable_expected = (
        f"notify-send, -i, {off_icon}, Disabling Keyboard..., Disconnected\n"
        "xinput, float, 20"
    )

    # patch attrs
    # ===========
    monkeypatch.setattr("kbtogglr._Popen", MockPopenXinputList)
    monkeypatch.setattr(
        "kbtogglr._appdirs.user_cache_dir", lambda x: str(cache_dir / x)
    )
    monkeypatch.setattr(
        "kbtogglr._call", lambda x, *_, **__: print(", ".join(x))
    )

    # run tests
    # =========
    # test when toggling off
    disable_output = main(capsys)

    # test when toggling on
    enable_output = main(capsys)

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
    monkeypatch.setattr("kbtogglr._Popen", MockPopenCommandNotFound)
    with pytest.raises(RuntimeError) as err:
        kbtogglr.main()

    assert str(err.value) == "cannot detect keyboard id"
