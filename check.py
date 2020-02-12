import yadisk
import re
from bz2 import BZ2File
import zipfile
import requests
import bz2

# def split_file(file, prefix, max_size, buffer=1024):
#     try:
#         with open(file, 'r+b') as src:
#             suffix = 0
#             while True:
#                 with open(prefix + '.%s' % suffix, 'w+b') as tgt:
#                     written = 0
#                     while written < max_size:
#                         data = src.read(buffer)
#                         if data:
#                             tgt.write(data)
#                             written += buffer
#                         else:
#                             return suffix
#                     suffix += 1
#     except FileNotFoundError:
#         print("Нет такого файла")
#
#
# split_file('hu.txt', 'kek.txt', 1000)

string = '<node id="3927953223" version="1" timestamp="2016-01-05T00:50:35Z" lat="53" lon="33"/>'
if re.match(r'<node id="', string) is not None:
    s = re.findall(r'[0-9]{2}.[0-9]+', string)
    print(s)
    coordinates = ([int(s[0]), float(s[4]), float(s[5])])
    print(coordinates)
