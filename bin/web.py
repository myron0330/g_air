"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: long run web service.
#   Author: Myron
# **********************************************************************************#
"""
from flask import Flask
from flask_restful import Api

server = Flask(__name__)
api = Api(server)


if __name__ == '__main__':
    server.run(host='0.0.0.0', debug=False, threaded=True, port=6666)
