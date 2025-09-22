from setuptools import setup


setup(
    name='pyqserver',
    version='0.0.1',
    packages=['pyqserver'],
    entry_points={
        'console_scripts': [
            'pyqserver = pyqserver.main:main'
        ]
    },
    install_requires=[
        'cirq>=1.5.0',
        'qiskit>=2.1.1',
        'qiskit-aer>=0.17.1',
        'qbraid>=0.9.10',
        'qsimcirq>=0.22.0',
    ]
)
