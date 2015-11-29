from setuptools import setup, find_packages

setup(
    name='uconfig',
    version='0.1',
    packages=['uconfig'],
    include_package_data=True,
    install_requires=[
        'pyyaml',
    ],
)
