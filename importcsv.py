import sys
import decimal
import pandas as pd


from hhs.models import HHSEntry

df = pandas.read_csv('whi.csv', sep=';', decimal=',', header=None)
print(df)

for i in range(len(df)): s= df.loc[i]; h = HHSEntry(player='jessica', date=s[0], where="", score=s[1],
													: cr=decimal.Decimal(float(s[2])), slope=s[3]); h.save()

ds = HHSEntry.objects.all()
