import os
from glob import glob

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

# get github workflow env vars
try:
    version = (os.environ['GIT_TAG_NAME']).replace('v', '')
except KeyError:
    print('Defaulting to 0.0.0')
    version = '0.0.0'

# get files to include in dist
dist_files = [file.replace('pytb/', '')
              for file in glob("pytb/reference_images/*/*.png")]

setup(
    name='py-tb',
    version=version,
    description='Automated Twitter Following',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    license='None',
    keywords='follow twitter bot',
    author='Matthew Miglio',
    url='https://github.com/matthewmiglio/py-tb',
    download_url='https://github.com/matthewmiglio/py-tb',
    install_requires=[
        'comtypes', 'cx-Freeze', 'cycler', 'fonttools',
        'joblib', 'keyboard', 'kiwisolver',
        'lief', 'matplotlib', 'MouseInfo',
        'numpy', 'opencv-python', 'packaging',
        'Pillow', 'PyAutoGUI', 'PyGetWindow',
        'PyMsgBox', 'pyparsing', 'pyperclip',
        'PyRect', 'PyScreeze', 'PySimpleGUI',
        'python-dateutil', 'pytweening', 'pywin32',
        'pywinauto', 'screeninfo', 'six',
    ],
    packages=['pytb'],
    include_package_data=True,
    package_data={'pytb': dist_files},
    python_requires='>=3.10',
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'pyclashbot = pytb.__main__:main_gui',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3.10',
    ],
)
