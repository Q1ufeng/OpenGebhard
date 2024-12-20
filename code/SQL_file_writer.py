from SQL_generator import SQL_generator

def SQL_file_writer (file_name,people_name_sqrt,book_num,SQL_numbase) :
    sqls = SQL_generator(people_name_sqrt,book_num,SQL_numbase)
    with open ("SQLs/"+file_name+".sql",'w') as f:
        for sql in sqls :
            f.write (sql)
            f.write ("\n")