import platform, os
import PyInstaller.__main__

class PyinstallerWrapper:
    def __init__(self, main_script_path, name=None, one_file=True, no_console=True):
        # Initialize class variables
        self.main_script_path = main_script_path
        self.name = name
        self.one_file = one_file
        self.no_console = no_console

        # Detect the current operating system
        self.os_name = platform.system()

        # Determine the PyInstaller command to use based on the operating system
        self.pyinstaller_cmd = self._get_pyinstaller_cmd()

        # Determine the PyInstaller options to use based on the operating system and class variables
        self.pyinstaller_opts = self._get_pyinstaller_opts()

    def _get_pyinstaller_cmd(self):
        # If the operating system is Windows, use the pyinstaller.exe command
        # Otherwise, use the pyinstaller command
        if self.os_name == "Windows":
            return 'pyinstaller.exe'
        return 'pyinstaller'

    def _get_pyinstaller_opts(self):
        # Set the PyInstaller options based on the class variables and operating system
        opts = ['--onefile'] if self.one_file else []
        if self.no_console:
            opts.append('--noconsole')
        if self.os_name == "Darwin" and self.name is not None:
            opts.append('--name={}'.format(self.name))
            opts.append('--windowed')
        return opts

    def build(self):
        # Change the current working directory to the directory containing the main script
        os.chdir(os.path.dirname(self.main_script_path))

        # Call PyInstaller to create an executable file for the main script
        PyInstaller.__main__.run(self.pyinstaller_opts + [self.main_script_path])