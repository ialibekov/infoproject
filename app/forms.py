#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'id': 'searchForm', 'class': 'form-control'}),
                            error_messages={'required': u'Введите запрос'})
