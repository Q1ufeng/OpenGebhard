import random
import info_generator


def SQL_generator(people_num_sqrt, book_num, SQL_numbase):
    in_SQLs = []
    deal_SQLs = []
    info = info_generator.info_generator(people_num_sqrt, book_num)
    people_names = info[0]
    people_addr = info[1]
    people_depo = info[2]
    book_names = info[3]
    book_stock = info[4]
    book_price = info[5]

    # sql to drop all previous tables (need to be commented at the first run)
    in_SQLs.append("DROP TABLE stock;")
    in_SQLs.append("DROP TABLE reader;")
    in_SQLs.append("DROP TABLE to_borrow;")
    in_SQLs.append("DROP TABLE borrowed;")
    in_SQLs.append("DROP TABLE giveback;")
    in_SQLs.append("DROP TABLE reader_stock;")
    in_SQLs.append("DROP TABLE purchase;")
    in_SQLs.append("DROP TABLE book_info;")

    # sql to initialize all tables
    in_SQLs.append("CREATE TABLE stock (id integer,book_name varchar(35),book_num integer,price integer);")
    in_SQLs.append(
        "CREATE TABLE reader (id integer,reader_name varchar(35),address varchar(35),deposit integer,cost integer);")
    in_SQLs.append("CREATE TABLE to_borrow(id integer,reader_id integer,book_id integer,borrow_num integer,dealt bool);")
    in_SQLs.append("CREATE TABLE borrowed(id integer,reader_id integer,book_id integer,book_num integer);")
    in_SQLs.append("CREATE TABLE giveback(id integer,reader_id integer,dealt bool);")
    in_SQLs.append("CREATE TABLE reader_stock(id integer,book_id integer,book_num integer,CONSTRAINT CONS1 UNIQUE (id, book_id));")
    in_SQLs.append("CREATE TABLE purchase(id integer,book_id integer,book_num integer,dealt bool);")
    in_SQLs.append("CREATE TABLE book_info(id integer,name varchar(35));")

    # sql to initialize useful functions
    in_SQLs.append("""CREATE OR REPLACE FUNCTION borrow_request()\
                    RETURNS VOID AS $$\
                    DECLARE\
                        can_borrow BOOLEAN;\
                    BEGIN\
                        CREATE TEMP TABLE temp_joined_table AS\
                        WITH joined_table AS (\
                            SELECT\
                                to_borrow.id AS to_borrow_id,\
                                to_borrow.reader_id AS reader_id,\
                                to_borrow.book_id AS book_id,\
                                i.name AS book_name,\
                                to_borrow.borrow_num AS borrow_num,\
                                s.book_num AS book_num,\
                                r.cost AS cost,\
                                r.deposit AS deposit,\
                                s.price AS price\
                            FROM to_borrow\
                            JOIN public.reader r ON r.id = to_borrow.reader_id\
                            JOIN public.book_info i ON i.id = to_borrow.book_id\
                            JOIN stock s ON s.book_name = i.name\
                            WHERE to_borrow.dealt = FALSE\
                        )\
                        SELECT * FROM joined_table;\
                    \
                        SELECT EXISTS (\
                            SELECT 1\
                            FROM temp_joined_table\
                            WHERE book_num >= borrow_num AND deposit - cost - price * borrow_num >= 0\
                        )\
                        INTO can_borrow;\
                    \
                        IF can_borrow THEN\
                            UPDATE to_borrow\
                            SET dealt = TRUE\
                            WHERE id IN (\
                                SELECT to_borrow_id\
                                FROM temp_joined_table\
                            );\
                    \
                            INSERT INTO borrowed(id, reader_id, book_id, book_num)\
                            SELECT to_borrow_id, reader_id, book_id, borrow_num\
                            FROM temp_joined_table;\
                    \
                            UPDATE reader\
                            SET cost = cost + (\
                                SELECT SUM(borrow_num * price)\
                                FROM temp_joined_table\
                            )\
                            WHERE reader.id IN (\
                                SELECT reader_id\
                                FROM temp_joined_table\
                            );\
                    \
                            UPDATE stock\
                            SET book_num = stock.book_num - subquery.borrow_num\
                            FROM (\
                                SELECT book_name, borrow_num\
                                FROM temp_joined_table\
                            ) AS subquery\
                            WHERE stock.book_name = subquery.book_name;\
                    \
                            INSERT INTO reader_stock (id, book_id, book_num)\
                            SELECT reader_id, book_id, SUM(borrow_num)\
                            FROM temp_joined_table\
                            GROUP BY reader_id, book_id\
                            ON CONFLICT (id, book_id)\
                            DO UPDATE\
                            SET book_num = reader_stock.book_num + EXCLUDED.book_num;\
                    \
                        ELSE\
                            UPDATE to_borrow\
                            SET dealt = 'true'\
                            WHERE id IN (\
                                SELECT to_borrow_id\
                                FROM temp_joined_table\
                            );\
                        END IF;\
                    DROP TABLE temp_joined_table;\
                    END;\
                    $$ LANGUAGE plpgsql;""")
    in_SQLs.append("""CREATE OR REPLACE FUNCTION giveback_request()\
                    RETURNS VOID AS $$\
                    DECLARE\
                        has_book BOOLEAN;\
                    BEGIN\
                        CREATE TEMP TABLE temp_joined_table AS\
                        WITH joined_table AS (\
                            SELECT\
                                giveback.id AS giveback_id,\
                                giveback.reader_id AS reader_id,\
                                rs.book_id AS book_id,\
                                rs.book_num AS book_num,\
                                I.name AS book_name,\
                                s.price AS price\
                            FROM giveback\
                            JOIN reader_stock rs ON rs.id = giveback.reader_id\
                            JOIN book_info i ON rs.book_id = i.id\
                            JOIN stock s ON rs.book_id = i.id\
                            WHERE giveback.dealt = FALSE\
                        )\
                        SELECT * FROM joined_table;\
                    \
                        SELECT EXISTS(\
                            SELECT 1\
                            FROM temp_joined_table\
                        )\
                        INTO has_book;\
                    \
                        IF has_book THEN\
                            DELETE FROM reader_stock\
                            WHERE reader_stock.id IN (\
                                SELECT reader_id\
                                FROM temp_joined_table\
                                );\
                    \
                            UPDATE reader\
                            SET cost = cost - (\
                                SELECT SUM(book_num*price)\
                                FROM temp_joined_table\
                                WHERE temp_joined_table.reader_id = reader.id\
                                )\
                            WHERE reader.reader_name IN (\
                                SELECT reader_name\
                                FROM temp_joined_table\
                                );\
                    \
                            UPDATE stock\
                            SET book_num = book_num + (\
                                SELECT SUM(book_num)\
                                FROM temp_joined_table\
                                WHERE temp_joined_table.book_name = stock.book_name\
                                )\
                            WHERE stock.book_name IN (\
                                SELECT book_name\
                                FROM temp_joined_table\
                                );\
                    \
                            UPDATE giveback\
                            SET dealt = TRUE\
                            WHERE id IN (\
                                SELECT giveback_id\
                                FROM temp_joined_table\
                                );\
                        ELSE\
                            UPDATE giveback\
                            SET dealt = TRUE\
                            WHERE id IN (\
                                SELECT giveback_id\
                                FROM temp_joined_table\
                                );\
                        END IF;\
                    DROP TABLE temp_joined_table;\
                    END;\
                    $$ LANGUAGE plpgsql;""")
    in_SQLs.append("""CREATE OR REPLACE FUNCTION purchase_request()\
                    RETURNS VOID AS $$\
                        BEGIN\
                            CREATE TEMP TABLE temp_joined_table AS\
                            WITH joined_table AS (\
                                SELECT\
                                    purchase.book_id AS book_id,\
                                    purchase.book_num AS book_num,\
                                    i.name AS book_name\
                                FROM purchase\
                                JOIN book_info i ON i.id = purchase.book_id\
                                WHERE purchase.dealt = FALSE\
                            )\
                            SELECT * FROM joined_table;\
                            UPDATE stock\
                            SET book_num = book_num + (\
                                SELECT SUM(book_num)\
                                FROM temp_joined_table\
                                )\
                            WHERE stock.book_name IN (\
                                SELECT book_name\
                                FROM temp_joined_table\
                                );\
                            UPDATE purchase\
                            SET dealt = TRUE\
                            WHERE id >= 0;\
                        DROP TABLE temp_joined_table;\
                        END;\
                    $$ LANGUAGE plpgsql;""")

    # sql to initialize the stock and the residents
    for i in range(book_num):
        in_SQLs.append(
            "INSERT INTO stock VALUES(" + str(i + 1) + ",'" + book_names[i] + "'," + str(book_stock[i]) + "," + str(
                book_price[i]) + ");")
        in_SQLs.append("INSERT INTO book_info VALUES("+str(i+1)+",'"+str(book_names[i])+"');")
    for i in range(people_num_sqrt * people_num_sqrt):
        in_SQLs.append(
            "INSERT INTO reader VALUES(" + str(i + 1) + ",'" + people_names[i] + "','" + people_addr[i] + "'," + str(
                people_depo[i]) + "," + "0" + ");")

    # define the order of sql types
    # 1 is borrow , 2 is return , 3 is buy
    order = [1] * (8 * SQL_numbase) + [2] * SQL_numbase + [3] * SQL_numbase
    random.shuffle(order)

    to_borrow_id = 1
    giveback_id = 1
    purchase_id = 1

    # generate in_SQLs
    for i in range(10 * SQL_numbase):
        if order[i] == 1:
            reader_id = random.randint(1, people_num_sqrt * people_num_sqrt)
            book_id = random.randint(1, book_num)
            borrow_num = random.randint(1, 3)
            deal_SQLs.append("INSERT INTO to_borrow VALUES(" + str(to_borrow_id) + "," + str(reader_id) + "," + str(
                book_id) + "," + str(borrow_num) + "," + "FALSE" + ");")
            deal_SQLs.append("SELECT borrow_request();")
            to_borrow_id = to_borrow_id + 1
        elif order[i] == 2:
            reader_id = random.randint(1, people_num_sqrt * people_num_sqrt)
            deal_SQLs.append("INSERT INTO giveback VALUES(" + str(giveback_id) + "," + str(reader_id)+ "," + "FALSE" + ");")
            deal_SQLs.append("SELECT giveback_request();")
            giveback_id = giveback_id + 1
        else:
            book_id = random.randint(1, book_num)
            buy_num = random.randint(1, 9)
            deal_SQLs.append(
                "INSERT INTO purchase VALUES(" + str(purchase_id) + "," + str(book_id) + "," + str(buy_num)+ "," + "FALSE" + ");")
            deal_SQLs.append("SELECT purchase_request();")
            purchase_id = purchase_id + 1

    return in_SQLs , deal_SQLs
