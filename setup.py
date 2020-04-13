from setuptools import setup

setup(
    name='riskquant',
    packages=['riskquant'],
    version='0.1.0',  # Increment on any tagged release, and change download_url
    license='apache-2.0',
    author='Netflix Detection team',
    author_email='detection@netflix.com',
    description='A library for applying quantitative risk models.',
    keywords='riskquant risk quantify statistics',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'License :: OSI Approved :: Apache Software License',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',
      'Programming Language :: Python :: 3.8',
      'Topic :: Security',
      'Intended Audience :: Information Technology',
      'Intended Audience :: Financial and Insurance Industry',
      'Intended Audience :: System Administrators',
      'Topic :: Office/Business :: Financial'
    ],
    url='https://github.com/Netflix-Skunkworks/riskquant',
    download_url='https://github.com/Netflix-Skunkworks/riskquant/archive/v0.1.0.tar.gz',  # Must be a tagged release
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
