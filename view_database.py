
import sqlite3


conn = sqlite3.connect('frozen_symbols.db')
c = conn.cursor()

c.execute('SELECT * FROM frozen_symbols')
rows = c.fetchall()

print('**************************************')
for row in rows:
    print(row)
print('**************************************')

conn.close()
