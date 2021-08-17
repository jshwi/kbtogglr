"""
setup
=====

``setuptools`` for package.
"""
import setuptools

with open("README.rst", "r") as readme:
    README = readme.read()


setuptools.setup(
    name="kbtogglr",
    version="0.1.0",
    description="Toggle keyboard on and off for xinput",
    long_description=README,
    long_description_content_type="text/x-rst",
    author="Stephen Whitlock",
    author_email="stephen@jshwisolutions.com",
    url="https://github.com/jshwi/kbtogglr",
    license="MIT",
    platforms="GNU/Linux",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    keywords=["keyboard", "xorg", "xserver", "xinput"],
    packages=setuptools.find_packages(exclude=["tests"]),
    include_package_data=True,
    zip_safe=False,
    entry_points={"console_scripts": ["kbtogglr=kbtogglr.__main__:main"]},
    data_files=[("share/applications", ["kbtogglr/lib/template.desktop"])],
    python_requires=">=3.8",
)
