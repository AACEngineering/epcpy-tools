import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()


setup(
    name='epc-encoding-utils',
    version=__import__('epc').__version__,
    description='Library for encoding/decoding and representing GS1 Electronic Product Codes',
    long_description=README,
    long_description_content_type='text/markdown',
    author='AAC Engineering',
    url='https://github.com/AACEngineering/epcpy-tools',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.5',
    install_requires=[
        'setuptools'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='epc,rfid,gid,giai,gid,grai,sgln,sgtin,encoding,decoding,barcodes',
)
