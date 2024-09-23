import sqlite3


username = 'Дима Красиков'
STMT_PRE = (
    'DELETE FROM Schedule WHERE user_id'
    '= (SELECT id FROM user WHERE name = ?)'
)
STMT = 'DELETE FROM User WHERE name = ?'
STMT_NEXT = 'SELECT * FROM User'


connection = sqlite3.connect('bwy_bot.db')
cursor = connection.cursor()

cursor.execute(STMT_PRE, (username,))
cursor.execute(STMT, (username,))
cursor.execute(STMT_NEXT)

results = cursor.fetchall()
print(results)
connection.commit()
connection.close()
