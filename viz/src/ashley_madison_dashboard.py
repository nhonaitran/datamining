import datetime
import sys
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config

def query_count_by_country():
  try:
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = "SELECT country, count(*) as total " \
      "FROM am_am_member " \
      "WHERE country is not null " \
      "GROUP BY country " \
      "ORDER BY country "
    cursor.execute(query)
    
    rows = cursor.fetchall()

    #print('Total Row(s):', cursor.rowcount)
    print('{},{}'.format('country', 'count'))
    for row in rows:
      print('{},{}'.format(row[0], row[1]))
      #print(row)

  except Error as e:
    print(e)

  finally:
    cursor.close()
    conn.close()

def query_members_by_created_date():
  query = "SELECT first_name, last_name, city, state, zip, longitude, latitude, createdon " \
    "FROM am_am_member " \
    "WHERE createdon BETWEEEN %s AND %s;"
  
  start_date = datetime.date(2015, 1, 1)
  end_date = datetime.date(2015, 7, 1)
  args = (start_date, end_date)

  try:
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()
    cursor.execute(query, args)
    rows = cursor.fetchall()

    print('Total Row(s):', cursor.rowcount)
    for row in rows:
      print(row)

  except Error as e:
    print(e)

  finally:
    cursor.close()
    conn.close()

def proc_member_info():
  try:
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()
    
    args = ['Jones', '']
    #args = ['', 'Amanda']
    #args = ('Jones', 'Amanda')
    cursor.callproc('get_member_info', args)
    
    for result in cursor.stored_results():
      rows = result.fetchall()
      #print('Total Row(s):', len(rows))
      for row in rows:
        print(row)
    
                  
  except Error as e:
    print(e)
  
  finally:
    cursor.close()
    conn.close()

def get_unique_states():
  try:
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()
    query_stmt = "SELECT distinct state FROM am_am_member WHERE state is not null ORDER BY state;"
    cursor.execute(query_stmt)

    rows = cursor.fetchall()
    for row in rows:
      print('insert into geocode_lookup (\'type\', code, name, long_name) values(2, {}, \' \', \' \')'.format(row[0]))
                     
  except Error as e:
    print(e)
  
  finally:
    cursor.close()
    conn.close()
  

if __name__ == '__main__':
  run_query = {0 : query_count_by_country,
               1 : query_members_by_created_date,
               2 : proc_member_info,
               3 : get_unique_states,
  }
  
  no = int(sys.argv[1])
  #no = 3
  #print(no)
  run_query[no]()

  
  #query_members_by_created_date()  --- this is not working... can't read the between x and y
  