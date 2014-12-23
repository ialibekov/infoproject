#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hunspell
import os

from app.models import TextDocument

class SpellChecker(object):
	def __init__(self):
		pwd = os.getcwd()
		self.checker = None
		path_dic = pwd + '/spell/ru_RU.dic'
		path_aff = pwd + '/spell/ru_RU.aff'
		if os.path.exists(path_dic) and os.path.exists(path_aff):
			print "Spell: have"
			self.checker = hunspell.HunSpell(path_dic, path_aff)
		else:
			print "Spell: do nothing"

	def spell(self, word):
		if self.checker is None:
			return word
		if self.checker.spell(word):
			return word
		else:
			suggest = self.checker.suggest(word)
			if suggest:
				return suggest[0]
		return word

