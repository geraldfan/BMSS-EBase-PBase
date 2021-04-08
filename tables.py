# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 15:22:22 2020

@author: Gerald
"""

from flask_table import Table, Col, LinkCol

# Overriding the Col class to format the content 
class FormatCol(Col):
    """Subclass of Col which formats the contents of the Col"""
    def td_format(self, content):
        output = []
        for char in content:
            if char == ',':
                char += '<br/>'
            output.append(char)
        return output
    
class ParameterBoundsCol(Col):
    """Subclass of Col which formats the contents of the parameter Col"""
    def td_format(self, content):
        output = []
        for char in content:
            if char ==']':
                char += '<br/>'
            output.append(char)
        return output
class DescriptionCol(Col):
    """Subclass of Col which formats the contents of the description Col"""
    def td_format(self, content):
        output = []
        title = ['t','i','t','l','e']
        author = ['a','u','t','h','o','r']
        journal = ['j','o','u','r','n','a','l']
        for i in range(len(content) - 1):
            if content[i] == '\\' and content[i + 1] == 'n':
                output.append("<br/>")
            elif content[i-1] == '\'':
                output.append(content[i].upper())
            elif content[i] == '!':
                output.append('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp')
            elif content[i] == 't':
                isTitle = self.capitalize(i, title, content)
                if isTitle == True:
                    output.append(content[i].upper())
                else:
                    output.append(content[i])
            elif content[i] == 'a':
                isAuthor = self.capitalize(i, author, content)
                if isAuthor:
                    output.append(content[i].upper())
                else:
                    output.append(content[i])
            elif content[i] == 'j':
                isJournal = self.capitalize(i, journal, content)
                if isJournal:
                    output.append(content[i].upper())
                else:
                    output.append(content[i])
                        
            elif not ((content[i] == 'n' and content [i - 1] == '\\') or (content[i] == '{' or content[i] == '\'' or content[i] == '}')):
                output.append(content[i])
        return output
    def capitalize(self,i, word, content):
        """Helper function to capitalize a word"""
        isWord = True
        for j in range(len(word)):
            if not(content[i] == word[j]):
                isWord = False
                break
            else:
                i += 1
        return isWord

# Result html table outputted on the website.
class Results(Table):
    """Class corresponding to the search results HTML table displayed on the website"""
    classes = ['blueTable']
    id = Col('Experimental ID')
    time = Col('Time')
    set_temperature = Col('Set Temperature')
    data_values = ParameterBoundsCol('Data Values')
    settings = LinkCol('Settings', 'settings', url_kwargs=dict(id='id'))

# Settings html table outputted on the website
class Settings(Table):
    """Class corresponding to the Settings HTML table displayed on the website"""
    classes = ['blueTable']
    id = Col('Experimental ID')
    measurement = Col('Measurement')
    experiment_type = Col('Experiment Type')
    temperature = Col('temperature')
    media = Col('media')
    plasmid_name = Col('Plasmid Name')
    equipment = Col('equipment')
    filepath = Col('filepath')
    date = Col('date')
    procedure_details = Col('Procedure Details')
    wells_info = Col('Wells Information')