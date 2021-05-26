from setuptools import setup

setup(
    name='aiida_toolbox_ffr',
    version='0.1.0',
    description='A group of tools to work with AiiDA',
    url='https://github.com/ramirezfranciscof/aiida-toolbox-ffr',
    author='Francisco F. Ramirez',
    author_email='ramirezfranciscof@gmail.com',
    license='MIT License',
    packages=['aiida_toolbox_ffr'],

    install_requires=[
        'aiida_core>=1.4.4',
        'lorem>=0.1.1',
        'numpy',
        ],

    classifiers=[
        "Framework :: AiiDA",
        "Intended Audience :: Developers",
        'Development Status :: 1 - Planning',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)

