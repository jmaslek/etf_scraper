import sqlite3
conn = sqlite3.connect('test.db')
conn.execute("CREATE TABLE ETF ( sym varchar , price float )")
conn.execute("insert into ETF VALUES('SPY', 420.00)")
conn.execute("insert into ETF VALUES('QQQ', 380.00)")
conn.commit()
conn.close()
