from SQL_generator import SQL_generator

def SQL_file_writer (file_name,people_name_sqrt,book_num,SQL_numbase) :
    x = SQL_generator(people_name_sqrt,book_num,SQL_numbase)
    with open ("SQLs/"+file_name+"_in.sql",'w') as f:
        for sql in x[0] :
            f.write (sql)
            f.write ("\n")

    with open ("SQLs/"+file_name+"_deal.sql",'w') as f:
        for sql in x[1] :
            f.write (sql)
            f.write ("\n")