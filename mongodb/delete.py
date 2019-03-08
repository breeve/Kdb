import pymongo
import re
import math
import uuid
import time
import xlrd
import xlwt
import openpyxl
import os

client = pymongo.MongoClient(host='localhost', port=27017)
K_db = client.K_db

K_db.personalTime.remove({})
K_db.personalinfo.remove({})
K_db.question_class_first.remove({})
K_db.question_class_secondary.remove({})
K_db.question_normal_first.remove({})
K_db.question_normal_secondary.remove({})
K_db.taskSelect.remove({})
K_db.user_check_args.remove({})