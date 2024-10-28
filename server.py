# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 00:57:25 2024

@author: ASUS
"""

from os import environ
from flask import Flask

app = Flask(__name__)
app.run(environ.get('PORT'))