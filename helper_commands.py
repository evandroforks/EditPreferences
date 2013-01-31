#coding: utf8
#################################### IMPORTS ###################################

# Sublime Libs
import sublime
import sublime_plugin

################################ HELPER COMMANDS ###############################

class GotoLineNumber(sublime_plugin.TextCommand):
    def run(self, edit, line):
        view = self.view
        view.sel().clear()
        line_region = sublime.Region(view.text_point(line-1, 0))
        
        view.sel().add(
            line_region
        )
        view.show(line_region, True)

class SelectRegions(sublime_plugin.TextCommand):
    def run(self, edit, regions):
        view = self.view
        view.sel().clear()
        for r in regions:
            view.sel().add(sublime.Region(*r))
        
        view.show(view.sel(), True)

class OpenFileEnhanced(sublime_plugin.WindowCommand):
    def run(self, file, line=None, regions=None, **kw):
        window = self.window
        kw['file'] = file
        window.run_command("open_file", kw)

        full_name = (file.replace("${packages}/", 
                                   sublime.packages_path() + '/'))
        
        open_file_view = self.window.find_open_file(full_name)
        
        def do():
            if open_file_view.is_loading():
                sublime.set_timeout(do, 10)
            else:
                if line is not None:
                    open_file_view.run_command (
                        'goto_line_number', dict(line=line))
                elif regions is not None:
                    open_file_view.run_command (
                        'select_regions', dict(regions=regions))
                
                window.focus_view(open_file_view)
        do()