from setuptools import setup

setup(
    name="plc-sniffer",
    version="0.1.0",
    py_modules=["plc_sniffer"],
    install_requires=[
        "scapy>=2.5.0",
    ],
)
