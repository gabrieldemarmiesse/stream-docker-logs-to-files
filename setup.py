from pathlib import Path

from setuptools import find_packages, setup

setup(
    name="stream-docker-logs-to-file",
    install_requires=Path("requirements.txt").read_text().splitlines(),
    packages=find_packages(),
    include_package_data=True,  # will read the MANIFEST.in
)
