from setuptools import setup


setup(
    name='qserver',
    version='0.0.2',
    packages=['qserver'],
    entry_points={
        'console_scripts': [
            'run_qserver = qserver.main:main'
        ]
    },
    install_requires=[
        'cirq>=1.5.0',
        'qiskit>=2.1.1',
    ]
)