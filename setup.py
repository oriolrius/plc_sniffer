from setuptools import setup, find_packages

setup(
    name="plc-sniffer",
    version="0.2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "scapy>=2.5.0",
    ],
)
