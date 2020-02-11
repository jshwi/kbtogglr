README
======
`Read the Docs <https://kbtogglr.readthedocs.io/en/latest/>`_ |
`Github Pages <https://jshwi.github.io/kbtogglr/index.html>`_


.. image:: https://travis-ci.org/jshwi/kbtogglr.svg?branch=master
    :target: https://travis-ci.org/jshwi/kbtogglr.svg?branch=master
    :alt: Build Status
.. image:: https://codecov.io/github/jshwi/kbtogglr/coverage.svg?branch=master
    :target: https://codecov.io/github/jshwi/kbtogglr?branch=master
    :alt: codecov.io
.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: Licence

When working at your desk it might be practical to position your USB keyboard on top of your
laptop

Without switching off your laptop keyboard you are likely to accidentally hit keys

This package automates the task of toggling your laptop keyboard on and off so you won't be
frustrated to use your USB keyboard again

Normally to switch off your keyboard in Linux you would run:

.. code-block:: console

    $ xinput list

    ⎡ Virtual core pointer                    	id=2	[master pointer  (3)]
    ⎜   ↳ Virtual core XTEST pointer              	id=4	[slave  pointer  (2)]
    ⎜   ↳ ELAN2097:00 04F3:274F                   	id=11	[slave  pointer  (2)]
    ⎜   ↳ DELL090C:00 06CB:CCA6 Mouse             	id=13	[slave  pointer  (2)]
    ⎜   ↳ DELL090C:00 06CB:CCA6 Touchpad          	id=14	[slave  pointer  (2)]
    ⎜   ↳ Ducky Ducky One2 SF RGB                 	id=21	[slave  pointer  (2)]
    ⎜   ↳ MX Master 2S Mouse                      	id=23	[slave  pointer  (2)]
    ⎣ Virtual core keyboard                   	id=3	[master keyboard (2)]
        ↳ Virtual core XTEST keyboard             	id=5	[slave  keyboard (3)]
        ↳ Power Button                            	id=6	[slave  keyboard (3)]
        ↳ Video Bus                               	id=7	[slave  keyboard (3)]
        ↳ Power Button                            	id=8	[slave  keyboard (3)]
        ↳ Sleep Button                            	id=9	[slave  keyboard (3)]
        ↳ Integrated_Webcam_HD: Integrate         	id=10	[slave  keyboard (3)]
        ↳ ELAN2097:00 04F3:274F                   	id=12	[slave  keyboard (3)]
        ↳ Dell WMI hotkeys                        	id=15	[slave  keyboard (3)]
        ↳ AT Translated Set 2 keyboard            	id=16	[slave  keyboard (3)]
..

You need this list to find the id of the device you are switching off:
without a bit of research knowing which device to pick is confusing
(AT Translated Set 2 keyboard)

.. code-block:: console

    $ xinput float 16
..

Then to switch back on you need the slave AND master:

.. code-block:: console

    $ xinput reattach 16 3
..

This isn't very difficult but this number can change and this procedure can quickly become tedious,
not to mention the frustration experienced when you realise you don't have your USB keyboard on
you

Thankfully, this package includes an application icon

Whilst in the project root set up is as simple as running:

.. code-block:: console

    $ python setup.py install
..

To install with python setuptools as well:

.. code-block:: console

    $ python setup.py install --package
..

If you decide you want to uninstall KBTogglr:

.. code-block:: console

    $ python setup.py uninstall
..

To run from the console:

.. code-block:: console

    $ python kbtogglr
..

Finally, you can add the KBTogglr icon to your favourites and simply left click with your mouse