import sublime, sublime_plugin, re, string

class HexToRGBACommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for selection in self.view.sel():
            word_region = self.view.word(selection)
            if not word_region.empty():
                rgba_css = self.convert_to_rgba_css(word_region)
                if rgba_css:
                    if (self.view.substr(word_region.begin()-1) == "#"):
                        tmp_region = sublime.Region(word_region.begin()-1, word_region.end())
                        self.view.replace(edit, tmp_region, rgba_css)
                    elif (self.view.substr(word_region.begin()) == "#"):
                        tmp_region = sublime.Region(word_region.begin(), word_region.end())
                        self.view.replace(edit, tmp_region, rgba_css)
                else:
                    print 'false'

    def hex_to_rgba(self, value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))+(1,)

    def convert_to_rgba_css(self, word_region):
        word = self.view.substr(word_region)
        
        re_hex_color = re.compile('#?([0-9a-fA-F]{3}([0-9a-fA-F]{3})?){1}$')
        match = re_hex_color.match(word)

        if match:
            rgba = self.hex_to_rgba(word)
            rgba_css = 'rgba(%s,%s,%s,%s)' % rgba
            return rgba_css

        return False
