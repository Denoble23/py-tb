import os

from cx_Freeze import Executable, setup

# get github workflow env vars
try:
    version = os.environ['GIT_TAG_NAME']
except KeyError:
    print('Defaulting to v0.0.0')
    version = 'v0.0.0'

product_name = 'py-tb'

bdist_msi_options = {
    'upgrade_code': '{494bebef-6fc5-42e5-98c8-d0b2e339750f}',
    'add_to_path': False,
    'initial_target_dir': f'[ProgramFilesFolder]\\{product_name}',
}

dependencies = [
    'comtypes', 'cycler',
    'joblib', 'keyboard', 'kiwisolver',
    'lief', 'matplotlib', 'six',
    'numpy', 'cv2', 'packaging',
    'PIL', 'pyautogui', 'pygetwindow',
    'pymsgbox', 'pyparsing', 'pyperclip',
    'pyrect', 'pyscreeze', 'PySimpleGUI',
    'pytweening', 'pywinauto', 'screeninfo',
]

build_exe_options = {
    'includes': dependencies,
    'include_files': [
        'README.md',
    ]}


# GUI applications require a different base on Windows
base = None
# if sys.platform == 'win32':
#    base = 'Win32GUI'

exe = Executable(
    script='pytb\\__main__.py',
    base=base,
    shortcut_name=f"{product_name} {version}",
    shortcut_dir="DesktopFolder",
)

setup(
    name=product_name,
    version=version.replace('v', ''),
    description='Automated Twitter Following',
    executables=[exe],
    options={
        'bdist_msi': bdist_msi_options,
        'build_exe': build_exe_options
    }
)
