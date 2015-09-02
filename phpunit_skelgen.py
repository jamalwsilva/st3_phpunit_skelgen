import sublime, sublime_plugin
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
        self.settings = sublime.load_settings('phpunit_skelgen.sublime-settings')
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
        region = sublime.Region(0, self.view.size())
        contents = self.view.substr(region)
        handle = open(current_file, "r")
        lines = handle.readlines()

        pn = re.compile(r'^namespace\s+([^\s|;]+)')
        pc = re.compile(r'^class\s+(\S+)')
        namespace = [ pn.match(line).group(1) for line in lines if pn.match(line) ].pop()
        class_name = [ pc.match(line).group(1) for line in lines if pc.match(line) ].pop()

        return namespace + '\\' + class_name

    def run(self, edit):
        """
        Called when sublime invoke generate_test command
        """
        settings = Settings(self.view)

        folders = self.view.window().folders()

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
                test_fullpath = folder + '/' + tests_path + test_file
                dirname = os.path.dirname(test_fullpath)

                subprocess.call(r'mkdir -p "%s"' % (dirname,), shell=True)

                # render phpunit-skelgen command
                cmd = r'%s %s --verbose --bootstrap="%s" "%s" "%s" "%s" "%s"' % (
                    skeleton_bin,
                    'generate-test',
                    bootstrap,
                    class_name,
                    current_file,
                    class_name + "Test",
                    test_fullpath
                )

                # print and execute generated shell command
                output = subprocess.check_output(cmd, shell=True, cwd=folder)
                print(output.decode("utf-8"))

                # open newly created file
                self.view.window().open_file(test_fullpath)



