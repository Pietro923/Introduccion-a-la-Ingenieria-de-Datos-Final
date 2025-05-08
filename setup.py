from setuptools import find_packages, setup

setup(
    name="dg_testing",
    packages=find_packages(exclude=["dg_testing_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
