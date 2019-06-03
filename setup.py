from setuptools import setup

setup(
    name='I2cCharDisplay',
    version='1.0.1',
    description='Raspberry Pi software library for controlling I²C character LCD and OLED Displays',
    long_description=open('README.md').read(),
    url='https://github.com/dcityorg/i2c-char-display-library-raspberrypi',
    author='Gary Muhonen',
    author_email='gary@dcity.org',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: System :: Hardware',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='RPi US2066 HD44780 I2C interface OLED LCD',
    py_modules=['I2cCharDisplay'],
    install_requires=['smbus'],    
)