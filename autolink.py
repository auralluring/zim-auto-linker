#!/usr/bin/env python
# -*- coding: utf-8 -*-


from zim.plugins import PluginClass
import logging
from zim.gui.pageview import PageViewExtension
from zim.actions import action, toggle_action
from zim.notebook import Path, Notebook, Page, NotebookExtension

logger = logging.getLogger('zim.plugins')
class AutoLinkPlugin(PluginClass):
	plugin_info = {
		'name': _('Auto Linker'), 
		'description': _('''\
Automatically adds links to specified pages while you type. (case-sensitve)
Modify the script to include what you want to link to, contact me if you want help with that.

Note: The names of the pages you want to automatically link to cannot have any form of punctuation, due to the way it "cleans" the word. I will not be trying to fix this.
'''), 
		'author': 'OreoThePony/ HorseLuvver'
	}

def clean(word, prefix="", suffix=""):
		punctuation = ['"', "'", '.', ',', ';', ':', '[', ']', '{', '}', '=', '+', '-', '_', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '~', '/', '?', '<', '>']
		if any([mark in word for mark in punctuation]):
			if word[0] in punctuation:
				
				return clean(word[1:], prefix + word[0], suffix)
			else:
				
				return clean(word[:-1], prefix, word[-1] + suffix)
		else:
			return word, prefix, suffix

class AutoLinkerPageViewExtension(PageViewExtension):
	def __init__(self, plugin, pageview):
		PageViewExtension.__init__(self, plugin, pageview)
		self.connectto(pageview.textview, 'end-of-word', self.on_end_of_word)
		

	def link_collector(self, notebook):
		linklist = {}
		if notebook == "Notebook": #change this to your notebook name
			f = open("") #path to the parent page text file (use slashes, not colons)
			for line in f.read().splitlines():
				if line[:3] == '[[+' and line[-2:] == ']]': #I'm assuming you just have a list of pages linked like [[+Name]]. If not, correct it.
					linklist[line[3:-2]] = "" + line[3:-2] #the path where the pages that will be linked to are (colons this time)
			f.close()
		return linklist
	
	def on_end_of_word(self, textview, start, end, word, char, editmode):
		buffer = textview.get_buffer()
		logger.debug("End of word")
		links = self.link_collector(buffer.notebook.name)
		clean_word, prefix, suffix = clean(word)
		logger.debug("Word: %s", clean_word)
		if clean_word in links.keys():
			with buffer.tmp_cursor(start):
				buffer.delete(start, end)
				buffer.insert_at_cursor(prefix)
				buffer.insert_link_at_cursor(clean_word, links[clean_word])
				buffer.insert_at_cursor(suffix)
			buffer.set_modified(True)
			textview.stop_emission('end_of_word')
		else: logger.debug(links)
