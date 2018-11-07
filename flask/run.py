#!/usr/bin/python3

import sys

from app import app
from datas import datas

#初始化数据库

app.run(host=sys.argv[1], debug = True)
