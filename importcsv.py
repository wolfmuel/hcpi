import pandas as pd
import sys

from hhs.models import HHSEntry

df = pandas.read_csv('whi.csv', sep=';', decimal=',', header=None)
print(df)
