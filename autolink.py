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
		if notebook == "telluris":
			f = open("Notebooks/telluris/Plot/Characters.txt")
			for line in f.read().splitlines():
				if line[:3] == '[[+' and line[-2:] == ']]':
					linklist[line[3:-2]] = "Plot:Characters:" + line[3:-2]
			f = open("Notebooks/telluris/World/Flora&Fauna/Animals.txt")
			for line in f.read().splitlines():
				if line[:3] == '[[+' and line[-2:] == ']]':
					linklist[line[3:-2]] = "World:Flora&Fauna:Animals:" + line[3:-2]
			f = open("Notebooks/telluris/World/Flora&Fauna/Plants.txt")
			for line in f.read().splitlines():
				if line[:3] == '[[+' and line[-2:] == ']]':
					linklist[line[3:-2]] = "World:Flora&Fauna:Plants:" + line[3:-2]
			f = open("Notebooks/telluris/World/Flora&Fauna/SentientRaces.txt")
			for line in f.read().splitlines():
				if line[:3] == '[[+' and line[-2:] == ']]':
					linklist[line[3:-2]] = "World:Flora&Fauna:SentientRaces:" + line[3:-2]
		elif notebook == 'Superstore':
			f = open("Notebooks/Superstore/Characters.txt")
			for line in f.read().splitlines():
				if line[:3] == '[[+' and line[-2:] == ']]':
					linklist[line[3:-2]] = "Characters:" + line[3:-2]
		return linklist
	
	def on_end_of_word(self, textview, start, end, word, char, editmode):
		buffer = textview.get_buffer()
		if not (buffer.page.basename == 'Characters' or buffer.page.basename == 'Animals' or buffer.page.basename == 'Plants' or buffer.page.basename == 'SentientRaces'):
			links = self.link_collector(buffer.notebook.name)
			clean_word, prefix, suffix = clean(word)
			if clean_word in links.keys():
				with buffer.tmp_cursor(start):
					buffer.delete(start, end)
					buffer.insert_at_cursor(prefix)
					buffer.insert_link_at_cursor(clean_word, links[clean_word])
					buffer.insert_at_cursor(suffix)
				buffer.set_modified(True)
				textview.stop_emission('end_of_word')
