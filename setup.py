from setuptools import setup

setup(
    name='magerestore',
    version='0.1',
    py_modules=['cli'],
    install_requires=[
        'Click>=6', 'paramiko>=1.16'
    ],
    entry_points={
        'console_scripts': [
            'magerestore=magerestore.cli:main'
        ]
    },
)
