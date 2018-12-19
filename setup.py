from setuptools import setup

setup(
    name='mcp3008',
    version='0.1a3',
    description='RPi_mcp3008 is a library to listen to the MCP3008 A/D converter chip, as described in the datasheet.',
    long_description=open('README.rst').read(),
    url='https://github.com/luxedo/RPi_mcp3008',
    author='Luiz Eduardo Nishino Gomes do Amaral',
    author_email='luizamaral306@gmail.com',
    license='GPL3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: System :: Hardware',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='RPi MCP3008 SPI interface',
    # packages=['mcp3008'],
    install_requires=['spidev'],
)
