#! /usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2018/3/12 下午9:21
# from jingfen.jingfen_app import create_app, d
# b

from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'hello world!'
    pass

if __name__ == '__main__':
    app.run(debug=True)