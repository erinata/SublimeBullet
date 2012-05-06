# -*- coding: UTF-8 -*-
import sublime
import sublime_plugin
import re

# TODO: Better multi line pasting behaviour (esp the bug that if you paste a 2 lines content, a * will be added to the end of the pasting )
#       Just check whether the line is a empty line before inserting
# TODO: Can try to write to keymap files during start of sublime text. So the when one change the settings it will change the keymapping
# TODO: Write a text file in the plugin to indicate whether the settings are updated or not. When updated, write the keymap file accordingly. 
# TODO: Also, put instruction text in the keymap file say they shouldn't manage the keymap file directly. If they really want to, they should put a false in the settings file "manage keymap autoamtically" part first.

class Bullet(sublime_plugin.EventListener):
  Modifying = False
  #is_markdown = False
  md_enabled = False
  rest_enabled = False
  file_type = 0
  last_line = 0
  last_pos = 0
  #selectors = []
  selector_array = []

  def __init__(self):
    s = sublime.load_settings("Bullet.sublime-settings")
    Bullet.md_enabled = s.get("markdown_bullet_enabled", True)
    Bullet.rest_enabled = s.get("restructuredtext_bullet_enabled", False)
    #Bullet.selector_array = selectors.split("|")
    #Bullet.selector_array = ["text.html.markdown"]

  def on_activated(self, view):
    md_score = 0
    rest_score = 0
    if Bullet.md_enabled:
      md_score = view.score_selector(0,'text.html.markdown')
    if Bullet.rest_enabled:
      rest_score = view.score_selector(0,'text.restructuredtext')
    if md_score > 0 and md_score >= rest_score:
      Bullet.file_type = 1
    elif rest_score > 0 and rest_score >= md_score:
      Bullet.file_type = 2
    else:
      Bullet.file_type = 0

    #for x in range(len(Bullet.selector_array)):
    #  if (view.score_selector(0,Bullet.selector_array[x]) > 0):
    #    Bullet.is_markdown = True
    #    Bullet.update_row(self, view)
    #    return
    #  else:
    #    Bullet.is_markdown = False
  
  def on_selection_modified(self, view):
    #if (Bullet.is_markdown):
    if (Bullet.file_type > 0):
      Bullet.update_row(self, view)
    
  def update_row(self, view):
    loc = view.sel()[0]
    Bullet.last_pos = loc.begin()
    row, col = view.rowcol(Bullet.last_pos)
    Bullet.last_line = row

  def on_modified(self, view):
    if Bullet.Modifying == False:
      Bullet.Modifying = True
      if Bullet.file_type == 1:
        loc = view.sel()[0]
        row, col = view.rowcol(loc.begin())
        point_last_row = view.text_point(row - 1,0)
        if (row - Bullet.last_line == 1):
          previous_line = view.substr(view.line(Bullet.last_pos))
          if row != 0 and previous_line != "":
            match_pattern = re.search("^( *|\t*)(\*|\-|\>|\+|[0-9]+(\.))(.*)",previous_line)
            if match_pattern != None:
              if match_pattern.group(4) == " " or match_pattern.group(4) == "":
                reg_remove = view.find("(\*|\-|\>|\+|[0-9]+\.)(.*)",point_last_row-1)
                edit = view.begin_edit()
                view.erase(edit,reg_remove)
                view.end_edit(edit)
              else:
                if match_pattern.group(2) == "*":
                  insertion = "* "
                elif match_pattern.group(2) == "-":
                  insertion = "- "
                elif match_pattern.group(2) == ">":
                  insertion = "> "
                elif match_pattern.group(2) == "+":
                  insertion = "+ "
                else:
                  match_number = re.search("[0-9]+",match_pattern.group(2))
                  if match_number != None:
                    last_number = int(match_number.group(0))
                    insertion = str(last_number+1) + match_pattern.group(3) + " "
                  else:
                    insertion = ""
                edit = view.begin_edit()
                view.insert(edit, loc.end(), insertion)
                view.end_edit(edit)
      elif Bullet.file_type == 2:
        loc = view.sel()[0]
        row, col = view.rowcol(loc.begin())
        point_last_row = view.text_point(row - 1,0)
        if (row - Bullet.last_line == 1):
          previous_line = view.substr(view.line(Bullet.last_pos))
          if row != 0 and previous_line != "":
            match_pattern = re.search(u"^( *|\t*)(\*|\-|\+|•|⁃|‣|#.|[0-9]+(\.))(.*)",previous_line)
            if match_pattern != None:
              if match_pattern.group(4) == " " or match_pattern.group(4) == "":
                reg_remove = view.find(u"(\*|\-|\+|•|⁃|‣|#.|[0-9]+\.)(.*)",point_last_row-1)
                edit = view.begin_edit()
                view.erase(edit,reg_remove)
                view.end_edit(edit)
              else:
                if match_pattern.group(2) == "*":
                  insertion = "* "
                elif match_pattern.group(2) == "-":
                  insertion = "- "
                elif match_pattern.group(2) == "+":
                  insertion = "+ "
                elif match_pattern.group(2) == u"•":
                  insertion = u"• "
                elif match_pattern.group(2) == u"⁃":
                  insertion = u"⁃ "
                elif match_pattern.group(2) == u"‣":
                  insertion = u"‣ "
                elif match_pattern.group(2) == "#.":
                  insertion = "#. "
                else:
                  match_number = re.search("[0-9]+",match_pattern.group(2))
                  if match_number != None:
                    last_number = int(match_number.group(0))
                    insertion = str(last_number+1) + match_pattern.group(3) + " "
                  else:
                    insertion = ""
                edit = view.begin_edit()
                view.insert(edit, loc.end(), insertion)
                view.end_edit(edit)
      
    Bullet.update_row(self, view)
    Bullet.Modifying = False