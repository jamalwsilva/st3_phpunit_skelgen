import sublime, sublime_plugin

class Settings():
    view = None
    settings = None

    def __init__(self, view):
        self.settings = sublime.load_settings('phpunit_skelgen.sublime-settings')
        self.project_settings = {}

        if sublime.active_window() is not None:
            project_settings = view.settings()
            if project_settings.has("phpunit_skelgen"):
                self.project_settings = project_settings.get('phpunit_skelgen')

    def get(self, key):
        if key in self.project_settings:
            return self.project_settings.get(key)

        return self.settings.get(key)


class GenerateTestCommand(sublime_plugin.TextCommand):

    def get_class_name(self, current_file):
        pass

    def run(self, edit):
        pass

