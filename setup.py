from setuptools import setup

setup(
    name='riskquant',
    versioning='build-id',
    author='detection',
    author_email='detection@netflix.com',
    keywords='riskquant',
    url='https://github.com/Netflix-Skunkworks/riskquant/browse',
    setup_requires=['setupmeta'],
    python_requires='>=3.4',
    install_requires=[
        'matplotlib',
        'numpy',
        'scipy'
    ],
    extras_require={
        'test': ['tox'],
    },
    scripts=['bin/riskquant'],
)
