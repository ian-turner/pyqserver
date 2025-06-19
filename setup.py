from setuptools import setup


setup(
    name='qserver',
    version='0.0.2',
    packages=['qserver'],
    entry_points={
        'console_scripts': [
            'run_qserver = qserver.main:main'
        ]
    }
)