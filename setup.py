from setuptools import setup

setup(
    name='riskquant',
    versioning='build-id',
    author='detection',
    author_email='detection@netflix.com',
    keywords='riskquant',
    url='https://github.com/Netflix-Skunkworks/riskquant/browse',
    setup_requires=['setupmeta'],
    python_requires='>=3.5, <3.8',
    install_requires=[
        'matplotlib',
        'numpy',
        'scipy',
        # Tensorflow probability is tested and stable against Tensorflow 2.1.0
        # https://github.com/tensorflow/probability/releases
        'tensorflow >= 2.1.0',
        'tensorflow_probability'
    ],
    extras_require={
        'test': ['tox'],
    },
    scripts=['bin/riskquant'],
)
