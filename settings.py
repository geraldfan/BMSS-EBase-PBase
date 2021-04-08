# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 10:41:58 2020

@author: Gerald
"""

from app import db
from data import Data

# Class for the "setting" table in the Mbase.db file
class Setting(db.Model):
    """Class corresponding to the Setting table in the MBase.db"""
    __tablename__ = "settings"
    
    id = db.Column(db.String, db.ForeignKey("data.id"), primary_key = True)
    measurement = db.Column(db.String)
    experiment_type = db.Column(db.String)
    temperature = db.Column(db.String)
    media = db.Column(db.String)
    plasmid_name = db.Column(db.String)
    equipment = db.Column(db.String)
    filepath = db.Column(db.String)
    date = db.Column(db.String)
    procedure_details = db.Column(db.String)
    wells_info = db.Column(db.String)
    
    data = db.relationship("Data", backref=db.backref("settings", order_by=id), lazy=True)
    
    def __repr__(self):
        return "{}".format(self.system_type)