import datetime
import mysql.connector

from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config

def connect():
  """ Connect to MySQL database """
  db_config = read_db_config()
  try:
    print('Connecting to MySQL database...')
    conn = MySQLConnection(**db_config)

    if conn.is_connected():
      print('Connection establised.')
    else:
      print('Connection failed.')

  except Error as e:
    print(e)

  finally:
    conn.close()
    print('Connection closed.')

def query_with_fetchone():
  try:
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()
    query_stmt = "SELECT * FROM am_am_member limit 3"
    cursor.execute(query_stmt)
    row = cursor.fetchone()
    while row is not None:
      print(row)
      row = cursor.fetchone()

  except Error as e:
    print(e)

  finally:
    cursor.close()
    conn.close()

def query_with_fetchall():
  try:
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()
    query_stmt = "SELECT * FROM am_am_member limit 3"
    cursor.execute(query_stmt)
    rows = cursor.fetchall()

    print('Total Row(s):', cursor.rowcount)
    for row in rows:
      print(row)

  except Error as e:
    print(e)

  finally:
    cursor.close()
    conn.close()

def iter_row(cursor, size=10):
  while True:
    rows = cursor.fetchmany(size)
    if not rows:
      break
    for row in rows:
      yield row

def query_with_fetchmany():
  try:
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query_stmt = "SELECT * FROM am_am_member limit 3"
    cursor.execute(query_stmt)

    for row in iter_row(cursor, 10):
      print(row)

  except Error as e:
    print(e)

  finally:
    cursor.close()
    conn.close()

if __name__ == '__main__':
  #connect()
  #query_with_fetchone()
  #query_with_fetchall()
  query_with_fetchmany()
