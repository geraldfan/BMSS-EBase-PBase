# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 15:36:19 2020

@author: Gerald
"""

from app import db

# Class for the "model" table in the Mbase.db file
class Data(db.Model):
    """Class corresponding to the model table in the MBase.db"""
    __tablename__ = "data"

    id = db.Column(db.String, primary_key=True)
    time = db.Column(db.String)
    set_temperature = db.Column(db.String)
    data_values = db.Column(db.String)



    def __repr__(self):
        return "{}".format(self.system_type)