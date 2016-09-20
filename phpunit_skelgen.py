import sublime
import sublime_plugin
import re
import os.path
import subprocess


class Settings():
    """
    Class that loads the necessary setting for running the generate_test
    command.
    """

    settings = None

    def __init__(self, view):
        """
        Loads plugin and project specific settings
        """
        settings_key = 'phpunit_skelgen.sublime-settings'

        self.settings = sublime.load_settings(settings_key)
        self.project_settings = {}

        if sublime.active_window() is not None:
            project_settings = view.settings()
            if project_settings.has("phpunit_skelgen"):
                self.project_settings = project_settings.get('phpunit_skelgen')

    def get(self, key):
        """
        If defined, gets the project specific settings. If not, tries the plugin
        settings.
        """
        if key in self.project_settings:
            return self.project_settings.get(key)

        return self.settings.get(key)


class GenerateTestCommand(sublime_plugin.TextCommand):
    """
    Defines the sublime text command

    Can be tested at the console:
    - view.run_command('generate_test')

    Or binding a key combination at Preferences => Key bindings - User:
    - { "keys": ["ctrl+k", "ctrl+g"], "command": "generate_test"}
    """

    def get_class_name(self, current_file):
        """
        Parsers the PHP class name of the current file

        Open the console and run 'view.file_name()' to know the current file.
        """
        handle = open(current_file, "r")
        lines = handle.readlines()

        pn = re.compile(r'^namespace\s+([^;]+)')
        pc = re.compile(r'^(?:abstract )?class\s+(\S+)')
        namespace_matches = [
            pn.match(line).group(1) for line in lines if pn.match(line)
        ]
        class_name_matches = [
            pc.match(line).group(1) for line in lines if pc.match(line)
        ]

        if namespace_matches and class_name_matches:
            namespace = namespace_matches.pop()
            class_name = class_name_matches.pop()
            return namespace + '\\' + class_name

        if class_name_matches:
            class_name = class_name_matches.pop()
            return class_name.pop()

    def run(self, edit):
        """
        Called when sublime invoke generate_test command
        """
        settings = Settings(self.view)

        folders = self.view.window().folders()

        base_path = settings.get('base_path') or ""
        skeleton_bin = settings.get('bin')
        bootstrap = settings.get('bootstrap')
        tests_path = settings.get('tests_path')

        current_file = self.view.file_name()

        for folder in folders:
            if current_file.startswith(folder):
                # parse the PHP class name
                class_name = self.get_class_name(current_file)

                # create dir tree before trying to write test file
                relative_path = current_file.replace(folder, '')
                test_file = relative_path.replace('.php', 'Test.php')
                stripped = re.sub(base_path, '', test_file)
                test_fullpath = folder + '/' + tests_path + stripped
                dirname = os.path.dirname(test_fullpath)

                subprocess.call(r'mkdir -p "%s"' % (dirname,), shell=True)

                # render phpunit-skelgen command
                command_format = self.get_command_format()
                cmd = command_format % (
                    skeleton_bin,
                    'generate-test',
                    bootstrap,
                    class_name,
                    current_file,
                    class_name + "Test",
                    test_fullpath
                )

                # print and execute generated shell command
                output = subprocess.check_output(
                    cmd, shell=True, cwd=folder + '/' + base_path
                )
                print(output.decode("utf-8"))

                # open newly created file
                self.view.window().open_file(test_fullpath)

    def get_command_format(self):
        """
        Return skelgen command format
        """
        return r'%s %s --verbose --bootstrap="%s" "%s" "%s" "%s" "%s"'
