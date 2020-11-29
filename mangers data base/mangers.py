import pylightxl as xl


db = xl.readxl(fn='Mangers.xlsx')
print(db.ws(ws='Sheet1').index(row=2, col=1))


