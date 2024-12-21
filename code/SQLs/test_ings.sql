DROP TABLE stock;
DROP TABLE reader;
DROP TABLE to_borrow;
DROP TABLE borrowed;
DROP TABLE giveback;
DROP TABLE reader_stock;
DROP TABLE purchase;
DROP TABLE book_info;
CREATE TABLE stock (id integer,book_name varchar(35),book_num integer,price integer);
CREATE TABLE reader (id integer,reader_name varchar(35),address varchar(35),deposit integer,cost integer);
CREATE TABLE to_borrow(id integer,reader_id integer,book_id integer,borrow_num integer,dealt bool);
CREATE TABLE borrowed(id integer,reader_id integer,book_id integer,book_num integer);
CREATE TABLE giveback(id integer,reader_id integer,dealt bool);
CREATE TABLE purchase(id integer,book_id integer,book_num integer,dealt bool);
CREATE TABLE book_info(id integer,name varchar(35));
CREATE TABLE reader_stock(id integer,book_id integer,book_num integer);
CREATE OR REPLACE FUNCTION borrow_request()
                            RETURNS VOID
                            LANGUAGE plpgsql
                            AS $$
                            DECLARE
                                can_borrow BOOLEAN;
                                reader_stock_exist BOOLEAN;
                            BEGIN
                                CREATE TEMP TABLE temp_joined_table AS
                                    WITH joined_table AS (
                                    SELECT
                                        to_borrow.id AS to_borrow_id,
                                        to_borrow.reader_id AS reader_id,
                                        to_borrow.book_id AS book_id,
                                        i.name AS book_name,
                                        to_borrow.borrow_num AS borrow_num,
                                        s.book_num AS book_num,
                                        r.cost AS cost,
                                        r.deposit AS deposit,
                                        s.price AS price
                                    FROM to_borrow
                                        JOIN public.reader r ON r.id = to_borrow.reader_id
                                        JOIN public.book_info i ON i.id = to_borrow.book_id
                                        JOIN stock s ON s.book_name = i.name
                                    WHERE to_borrow.dealt = FALSE                        )
                                    SELECT * FROM joined_table;
                                SELECT EXISTS (
                                     SELECT 1
                                     FROM temp_joined_table
                                     WHERE book_num >= borrow_num AND deposit - cost - price * borrow_num >= 0
                                     )                        INTO can_borrow;
                                IF can_borrow THEN
                                    UPDATE to_borrow
                                    SET dealt = TRUE
                                    WHERE id IN (
                                                      SELECT to_borrow_id
                                                      FROM temp_joined_table
                                                      );
                                    INSERT INTO borrowed(id, reader_id, book_id, book_num)
                                    SELECT to_borrow_id, reader_id, book_id, borrow_num
                                    FROM temp_joined_table;
                                    UPDATE reader
                                    SET cost = cost + (
                                                   SELECT SUM(borrow_num * price)
                                                   FROM temp_joined_table
                                                   )
                                    WHERE reader.id IN (
                                            SELECT reader_id
                                            FROM temp_joined_table
                                            );
                                    UPDATE stock
                                    SET book_num = stock.book_num - subquery.borrow_num
                                    FROM (
                                               SELECT book_name, borrow_num
                                               FROM temp_joined_table
                                               ) AS subquery
                                    WHERE stock.book_name = subquery.book_name;
                        
                                    SELECT EXISTS (
                                        SELECT 1
                                        FROM temp_joined_table , reader_stock
                                        WHERE reader_id = reader_stock.id AND temp_joined_table.book_id = reader_stock.book_id
                                    ) INTO reader_stock_exist ;
                        
                                    IF reader_stock_exist THEN
                                        UPDATE reader_stock
                                        SET book_num = reader_stock.book_num +  (
                                            SELECT SUM (borrow_num)
                                            FROM temp_joined_table
                                            )
                                        WHERE reader_stock.id IN (
                                            SELECT reader_id
                                            FROM temp_joined_table
                                            );
                        
                                    ELSE
                                        INSERT INTO reader_stock (id, book_id, book_num)
                                        SELECT reader_id, book_id, SUM(borrow_num)
                                        FROM temp_joined_table
                                        GROUP BY reader_id, book_id;
                                    END IF;
                        
                        
                                    ELSE
                                        UPDATE to_borrow
                                        SET dealt = 'true'
                                        WHERE id IN (
                                                              SELECT to_borrow_id
                                                              FROM temp_joined_table
                                                              );
                                        END IF;
                                DROP TABLE temp_joined_table;
                                END;                    $$;
CREATE OR REPLACE FUNCTION giveback_request()                    RETURNS VOID                      LANGUAGE plpgsql                    AS $$                    DECLARE                        has_book BOOLEAN;                    BEGIN                        CREATE TEMP TABLE temp_joined_table AS                        WITH joined_table AS (                            SELECT                                giveback.id AS giveback_id,                                giveback.reader_id AS reader_id,                                rs.book_id AS book_id,                                rs.book_num AS book_num,                                I.name AS book_name,                                s.price AS price                            FROM giveback                            JOIN reader_stock rs ON rs.id = giveback.reader_id                            JOIN book_info i ON rs.book_id = i.id                            JOIN stock s ON rs.book_id = i.id                            WHERE giveback.dealt = FALSE                        )                        SELECT * FROM joined_table;                                            SELECT EXISTS(                            SELECT 1                            FROM temp_joined_table                        )                        INTO has_book;                                            IF has_book THEN                            DELETE FROM reader_stock                            WHERE reader_stock.id IN (                                SELECT reader_id                                FROM temp_joined_table                                );                                                UPDATE reader                            SET cost = cost - (                                SELECT SUM(book_num*price)                                FROM temp_joined_table                                WHERE temp_joined_table.reader_id = reader.id                                )                            WHERE reader.reader_name IN (                                SELECT reader_name                                FROM temp_joined_table                                );                                                UPDATE stock                            SET book_num = book_num + (                                SELECT SUM(book_num)                                FROM temp_joined_table                                WHERE temp_joined_table.book_name = stock.book_name                                )                            WHERE stock.book_name IN (                                SELECT book_name                                FROM temp_joined_table                                );                                                UPDATE giveback                            SET dealt = TRUE                            WHERE id IN (                                SELECT giveback_id                                FROM temp_joined_table                                );                        ELSE                            UPDATE giveback                            SET dealt = TRUE                            WHERE id IN (                                SELECT giveback_id                                FROM temp_joined_table                                );                        END IF;                    DROP TABLE temp_joined_table;                    END;                    $$;
CREATE OR REPLACE FUNCTION purchase_request()                    RETURNS VOID                      LANGUAGE plpgsql                     AS $$                        BEGIN                            CREATE TEMP TABLE temp_joined_table AS                            WITH joined_table AS (                                SELECT                                    purchase.book_id AS book_id,                                    purchase.book_num AS book_num,                                    i.name AS book_name                                FROM purchase                                JOIN book_info i ON i.id = purchase.book_id                                WHERE purchase.dealt = FALSE                            )                            SELECT * FROM joined_table;                            UPDATE stock                            SET book_num = book_num + (                                SELECT SUM(book_num)                                FROM temp_joined_table                                )                            WHERE stock.book_name IN (                                SELECT book_name                                FROM temp_joined_table                                );                            UPDATE purchase                            SET dealt = TRUE                            WHERE id >= 0;                        DROP TABLE temp_joined_table;                        END;                    $$;
INSERT INTO stock VALUES(1,'znqlgr',93,22);
INSERT INTO book_info VALUES(1,'znqlgr');
INSERT INTO stock VALUES(2,'truwxoteddfoeodfmvptoitupyi',144,37);
INSERT INTO book_info VALUES(2,'truwxoteddfoeodfmvptoitupyi');
INSERT INTO stock VALUES(3,'woxfekmwjfdvwtxagx',173,26);
INSERT INTO book_info VALUES(3,'woxfekmwjfdvwtxagx');
INSERT INTO stock VALUES(4,'jawgvhybshrepfkbnfsqrz',125,23);
INSERT INTO book_info VALUES(4,'jawgvhybshrepfkbnfsqrz');
INSERT INTO stock VALUES(5,'vzxpijgqmuoshj',31,32);
INSERT INTO book_info VALUES(5,'vzxpijgqmuoshj');
INSERT INTO stock VALUES(6,'pobzzuutwomfmvjiumtyubzld',34,27);
INSERT INTO book_info VALUES(6,'pobzzuutwomfmvjiumtyubzld');
INSERT INTO stock VALUES(7,'sgrlzxrkjwsepykjastteywwmubrc',161,20);
INSERT INTO book_info VALUES(7,'sgrlzxrkjwsepykjastteywwmubrc');
INSERT INTO stock VALUES(8,'uvc',18,34);
INSERT INTO book_info VALUES(8,'uvc');
INSERT INTO stock VALUES(9,'jelxv',139,28);
INSERT INTO book_info VALUES(9,'jelxv');
INSERT INTO stock VALUES(10,'wsmek',126,20);
INSERT INTO book_info VALUES(10,'wsmek');
INSERT INTO stock VALUES(11,'bikdeglojd',145,26);
INSERT INTO book_info VALUES(11,'bikdeglojd');
INSERT INTO stock VALUES(12,'fobzjryxefbkfqhfovclwgykqbkmmw',10,27);
INSERT INTO book_info VALUES(12,'fobzjryxefbkfqhfovclwgykqbkmmw');
INSERT INTO stock VALUES(13,'nhiqaovtzuwjrcymbcpahhjxao',124,27);
INSERT INTO book_info VALUES(13,'nhiqaovtzuwjrcymbcpahhjxao');
INSERT INTO stock VALUES(14,'prpexdh',36,23);
INSERT INTO book_info VALUES(14,'prpexdh');
INSERT INTO stock VALUES(15,'jtdcwnfaohshwfzqdk',111,30);
INSERT INTO book_info VALUES(15,'jtdcwnfaohshwfzqdk');
INSERT INTO stock VALUES(16,'geovixcwq',59,28);
INSERT INTO book_info VALUES(16,'geovixcwq');
INSERT INTO stock VALUES(17,'zthiozjiuhnqyhw',70,25);
INSERT INTO book_info VALUES(17,'zthiozjiuhnqyhw');
INSERT INTO stock VALUES(18,'puplcguoaquufaoszzufjtdvvyrtwm',12,25);
INSERT INTO book_info VALUES(18,'puplcguoaquufaoszzufjtdvvyrtwm');
INSERT INTO stock VALUES(19,'kwwms',9,34);
INSERT INTO book_info VALUES(19,'kwwms');
INSERT INTO stock VALUES(20,'puxlnatjtfeavuhchfx',13,40);
INSERT INTO book_info VALUES(20,'puxlnatjtfeavuhchfx');
INSERT INTO stock VALUES(21,'pmhsyeziva',199,29);
INSERT INTO book_info VALUES(21,'pmhsyeziva');
INSERT INTO stock VALUES(22,'iqpvqxngr',120,36);
INSERT INTO book_info VALUES(22,'iqpvqxngr');
INSERT INTO stock VALUES(23,'csxheppuyblnnokmvsfmtdblsgpms',170,36);
INSERT INTO book_info VALUES(23,'csxheppuyblnnokmvsfmtdblsgpms');
INSERT INTO stock VALUES(24,'npuhynfq',87,40);
INSERT INTO book_info VALUES(24,'npuhynfq');
INSERT INTO stock VALUES(25,'ftraddwkcgftwdksuuepluxhpi',104,21);
INSERT INTO book_info VALUES(25,'ftraddwkcgftwdksuuepluxhpi');
INSERT INTO stock VALUES(26,'npvuxushifm',181,33);
INSERT INTO book_info VALUES(26,'npvuxushifm');
INSERT INTO stock VALUES(27,'frlmcasl',154,27);
INSERT INTO book_info VALUES(27,'frlmcasl');
INSERT INTO stock VALUES(28,'nvpopkxiwfprlmh',123,33);
INSERT INTO book_info VALUES(28,'nvpopkxiwfprlmh');
INSERT INTO stock VALUES(29,'atiufuuiarukgt',130,27);
INSERT INTO book_info VALUES(29,'atiufuuiarukgt');
INSERT INTO stock VALUES(30,'mclqdksgehv',125,34);
INSERT INTO book_info VALUES(30,'mclqdksgehv');
INSERT INTO stock VALUES(31,'lfauwcckpem',49,33);
INSERT INTO book_info VALUES(31,'lfauwcckpem');
INSERT INTO stock VALUES(32,'xumolcqstcfmdq',124,22);
INSERT INTO book_info VALUES(32,'xumolcqstcfmdq');
INSERT INTO stock VALUES(33,'fscjbxiunmfsmkerzgsgd',176,25);
INSERT INTO book_info VALUES(33,'fscjbxiunmfsmkerzgsgd');
INSERT INTO stock VALUES(34,'smtatdkahlnttkhjwblgsg',48,29);
INSERT INTO book_info VALUES(34,'smtatdkahlnttkhjwblgsg');
INSERT INTO stock VALUES(35,'mwkimjekixnojupssetkbz',8,38);
INSERT INTO book_info VALUES(35,'mwkimjekixnojupssetkbz');
INSERT INTO stock VALUES(36,'qomsnxpocemrrunxpgqrp',84,40);
INSERT INTO book_info VALUES(36,'qomsnxpocemrrunxpgqrp');
INSERT INTO stock VALUES(37,'ayexnmjokttgdvyujonm',128,29);
INSERT INTO book_info VALUES(37,'ayexnmjokttgdvyujonm');
INSERT INTO stock VALUES(38,'oozpvppevg',200,20);
INSERT INTO book_info VALUES(38,'oozpvppevg');
INSERT INTO stock VALUES(39,'bzucjpwilulk',89,30);
INSERT INTO book_info VALUES(39,'bzucjpwilulk');
INSERT INTO stock VALUES(40,'gdhfknab',87,40);
INSERT INTO book_info VALUES(40,'gdhfknab');
INSERT INTO stock VALUES(41,'jbwv',137,39);
INSERT INTO book_info VALUES(41,'jbwv');
INSERT INTO stock VALUES(42,'rbefcebf',145,31);
INSERT INTO book_info VALUES(42,'rbefcebf');
INSERT INTO stock VALUES(43,'rxmegcqs',106,27);
INSERT INTO book_info VALUES(43,'rxmegcqs');
INSERT INTO stock VALUES(44,'kzm',11,25);
INSERT INTO book_info VALUES(44,'kzm');
INSERT INTO stock VALUES(45,'dlvfwzzuguezpswvvgtcmkpqoepwnw',49,27);
INSERT INTO book_info VALUES(45,'dlvfwzzuguezpswvvgtcmkpqoepwnw');
INSERT INTO stock VALUES(46,'stbblxe',32,20);
INSERT INTO book_info VALUES(46,'stbblxe');
INSERT INTO stock VALUES(47,'xuxurnrzopdonrnwoxk',181,33);
INSERT INTO book_info VALUES(47,'xuxurnrzopdonrnwoxk');
INSERT INTO stock VALUES(48,'gdwwlbmpwyvsvono',172,26);
INSERT INTO book_info VALUES(48,'gdwwlbmpwyvsvono');
INSERT INTO stock VALUES(49,'tkditrqefbddonzwqmhemribxjwil',126,33);
INSERT INTO book_info VALUES(49,'tkditrqefbddonzwqmhemribxjwil');
INSERT INTO stock VALUES(50,'gwnj',97,25);
INSERT INTO book_info VALUES(50,'gwnj');
INSERT INTO reader VALUES(1,'stmcgo-nhqj','jgsoslibirfvagkpzrrassmiu',104,0);
INSERT INTO reader VALUES(2,'stmcgo-wnfe','deczmauavalpmzwvmezkyddkvrser',189,0);
INSERT INTO reader VALUES(3,'stmcgo-adcs','kydznetevvewiwkpcuzybdw',150,0);
INSERT INTO reader VALUES(4,'stmcgo-dfhpuj','vapetzvjqvqbyoenadqaxnpdarhje',74,0);
INSERT INTO reader VALUES(5,'stmcgo-kjtm','joogwdllfjdstwhhk',97,0);
INSERT INTO reader VALUES(6,'stmcgo-oikbnytnyl','cjvwpddxchjzeettwvmgvnnuo',175,0);
INSERT INTO reader VALUES(7,'stmcgo-zhvb','fxzuzjkybtmhrjgulamwupkiew',157,0);
INSERT INTO reader VALUES(8,'stmcgo-jhaiec','ckquusrxdzummoxwja',139,0);
INSERT INTO reader VALUES(9,'stmcgo-grhozm','tgqbjiwgbfalwgorhirkat',135,0);
INSERT INTO reader VALUES(10,'stmcgo-otk','xvainmhuasxgjcf',81,0);
INSERT INTO reader VALUES(11,'ivsjokzy-nhqj','zmimypxvgr',127,0);
INSERT INTO reader VALUES(12,'ivsjokzy-wnfe','rdsufpdqwhszsoephmcjrrh',69,0);
INSERT INTO reader VALUES(13,'ivsjokzy-adcs','oqxkjhbwwfa',115,0);
INSERT INTO reader VALUES(14,'ivsjokzy-dfhpuj','zwmjdqhgryymmjcaacipkzgaldgbj',102,0);
INSERT INTO reader VALUES(15,'ivsjokzy-kjtm','noilblagclyrub',157,0);
INSERT INTO reader VALUES(16,'ivsjokzy-oikbnytnyl','rzdgmxsarn',172,0);
INSERT INTO reader VALUES(17,'ivsjokzy-zhvb','wnmwfrqishd',176,0);
INSERT INTO reader VALUES(18,'ivsjokzy-jhaiec','pckfihtfsh',157,0);
INSERT INTO reader VALUES(19,'ivsjokzy-grhozm','cvgfkzqjqectfuawt',166,0);
INSERT INTO reader VALUES(20,'ivsjokzy-otk','oetdjvqwhceauqswfjwjyp',104,0);
INSERT INTO reader VALUES(21,'fdqjgxdsy-nhqj','ivhkhkaxhusry',117,0);
INSERT INTO reader VALUES(22,'fdqjgxdsy-wnfe','yenzrasxmc',94,0);
INSERT INTO reader VALUES(23,'fdqjgxdsy-adcs','esbxyesvdhsvnwyhdxqlhdl',97,0);
INSERT INTO reader VALUES(24,'fdqjgxdsy-dfhpuj','mysuyhgwrpzbtcdjmqcvbpf',138,0);
INSERT INTO reader VALUES(25,'fdqjgxdsy-kjtm','obuoivueopkxgfiuczkogkmnj',71,0);
INSERT INTO reader VALUES(26,'fdqjgxdsy-oikbnytnyl','mocppgoktvfmmjjankkrd',77,0);
INSERT INTO reader VALUES(27,'fdqjgxdsy-zhvb','hfucgphipjqghxjnqhgongsfps',50,0);
INSERT INTO reader VALUES(28,'fdqjgxdsy-jhaiec','olbldavwutzv',84,0);
INSERT INTO reader VALUES(29,'fdqjgxdsy-grhozm','hknbfvmoiuf',87,0);
INSERT INTO reader VALUES(30,'fdqjgxdsy-otk','gpkomcgdwkzrmiqfwxighnaedq',162,0);
INSERT INTO reader VALUES(31,'aqovtf-nhqj','zecapuhquew',129,0);
INSERT INTO reader VALUES(32,'aqovtf-wnfe','umkcmgpiqlpmmgghio',146,0);
INSERT INTO reader VALUES(33,'aqovtf-adcs','hvixmsityxj',166,0);
INSERT INTO reader VALUES(34,'aqovtf-dfhpuj','vfhswpobaoxj',160,0);
INSERT INTO reader VALUES(35,'aqovtf-kjtm','sllnfsdweusrbnws',152,0);
INSERT INTO reader VALUES(36,'aqovtf-oikbnytnyl','fpokaonfttdflrkcozzmfiyn',183,0);
INSERT INTO reader VALUES(37,'aqovtf-zhvb','qyctcsgklvqnzjer',98,0);
INSERT INTO reader VALUES(38,'aqovtf-jhaiec','zedhzqpguhrcehlcqrstnor',147,0);
INSERT INTO reader VALUES(39,'aqovtf-grhozm','ttlebfgavjexetknijbatjqrmntpm',165,0);
INSERT INTO reader VALUES(40,'aqovtf-otk','tbfikcuuezszoodmkcqacdsvxw',166,0);
INSERT INTO reader VALUES(41,'djdcxt-nhqj','bjjpjqnqkgnordhvnriv',170,0);
INSERT INTO reader VALUES(42,'djdcxt-wnfe','syadjiuaizsuhiazboxkjahlkk',189,0);
INSERT INTO reader VALUES(43,'djdcxt-adcs','ispctojkfngnaqodjkdzhjqkehchx',140,0);
INSERT INTO reader VALUES(44,'djdcxt-dfhpuj','szxmowlooqlsxskipks',128,0);
INSERT INTO reader VALUES(45,'djdcxt-kjtm','ghqhmnmxqvqxljuwxlo',80,0);
INSERT INTO reader VALUES(46,'djdcxt-oikbnytnyl','kbjnbosudxhmmyhjo',169,0);
INSERT INTO reader VALUES(47,'djdcxt-zhvb','hkalfieybpbt',139,0);
INSERT INTO reader VALUES(48,'djdcxt-jhaiec','qwsweqbvjof',58,0);
INSERT INTO reader VALUES(49,'djdcxt-grhozm','aoviixltwphyilndcpywky',51,0);
INSERT INTO reader VALUES(50,'djdcxt-otk','aqdrjfaddjvdywmluklsexdw',112,0);
INSERT INTO reader VALUES(51,'rrqn-nhqj','ojyjsfhpegncktnedblgxhoy',163,0);
INSERT INTO reader VALUES(52,'rrqn-wnfe','zyvjywjoegyerhgt',79,0);
INSERT INTO reader VALUES(53,'rrqn-adcs','bzbmwrqmfkqwpgrzyhh',148,0);
INSERT INTO reader VALUES(54,'rrqn-dfhpuj','avezudfvorxhlbhuvoen',55,0);
INSERT INTO reader VALUES(55,'rrqn-kjtm','ajvmjygknblxm',143,0);
INSERT INTO reader VALUES(56,'rrqn-oikbnytnyl','qdqjowlussyvzevujvtao',197,0);
INSERT INTO reader VALUES(57,'rrqn-zhvb','dtjlsbfhziryeeywtno',171,0);
INSERT INTO reader VALUES(58,'rrqn-jhaiec','xlqpocnfhedhqj',169,0);
INSERT INTO reader VALUES(59,'rrqn-grhozm','pnvlfebcsvogr',75,0);
INSERT INTO reader VALUES(60,'rrqn-otk','xypqeznsuejtwqclmmyfuispm',127,0);
INSERT INTO reader VALUES(61,'rwbn-nhqj','zpfhxgrwdwwrizwyfvs',187,0);
INSERT INTO reader VALUES(62,'rwbn-wnfe','ojoozfuzytevw',54,0);
INSERT INTO reader VALUES(63,'rwbn-adcs','xhbhboifaxhucigxubm',56,0);
INSERT INTO reader VALUES(64,'rwbn-dfhpuj','crgbvnailreygfpldwxktm',170,0);
INSERT INTO reader VALUES(65,'rwbn-kjtm','aaidothmaksmkvztvzdqlpfzack',116,0);
INSERT INTO reader VALUES(66,'rwbn-oikbnytnyl','pohqpkhsygbornxmzhopvzcbd',188,0);
INSERT INTO reader VALUES(67,'rwbn-zhvb','ohakhpzwsrftldtifh',153,0);
INSERT INTO reader VALUES(68,'rwbn-jhaiec','dkmujeomoslxpmwjnoiugaidiwl',157,0);
INSERT INTO reader VALUES(69,'rwbn-grhozm','laelkrhlbehampwlrfb',64,0);
INSERT INTO reader VALUES(70,'rwbn-otk','ozqtshxaronq',129,0);
INSERT INTO reader VALUES(71,'mdjej-nhqj','rukzmuvahbrhje',99,0);
INSERT INTO reader VALUES(72,'mdjej-wnfe','zazopyqjjsqtvdlnkvcmnkuxuxvyz',139,0);
INSERT INTO reader VALUES(73,'mdjej-adcs','nbnhlhlblftdewtssu',188,0);
INSERT INTO reader VALUES(74,'mdjej-dfhpuj','bvoklqteohmbbrbogxk',184,0);
INSERT INTO reader VALUES(75,'mdjej-kjtm','qpzsgzorikpevnopuwdyrkqgplbavx',99,0);
INSERT INTO reader VALUES(76,'mdjej-oikbnytnyl','hojrewirvpniwnbjl',151,0);
INSERT INTO reader VALUES(77,'mdjej-zhvb','grahegeqtegkkvjxmwhzwtp',71,0);
INSERT INTO reader VALUES(78,'mdjej-jhaiec','ocoiqoejxsaopzjbayzwtkdgqbbt',190,0);
INSERT INTO reader VALUES(79,'mdjej-grhozm','vfjwgjcfecsordodulixpfwxxjv',84,0);
INSERT INTO reader VALUES(80,'mdjej-otk','pjjbdhxxrvxonezhswsiu',80,0);
INSERT INTO reader VALUES(81,'lznr-nhqj','ezxjzsledeljaffq',155,0);
INSERT INTO reader VALUES(82,'lznr-wnfe','ktbmlekmnzhposumfxyhzvblaed',63,0);
INSERT INTO reader VALUES(83,'lznr-adcs','phitlntyxninrmnh',148,0);
INSERT INTO reader VALUES(84,'lznr-dfhpuj','nrujxrzlmyqaacdlpyurdgempuxoub',173,0);
INSERT INTO reader VALUES(85,'lznr-kjtm','vvtjfyimrrybwqddotrtlws',183,0);
INSERT INTO reader VALUES(86,'lznr-oikbnytnyl','rfalsnsimktgqptpok',107,0);
INSERT INTO reader VALUES(87,'lznr-zhvb','tirzxhywwdohitbygzniarlppbejlz',120,0);
INSERT INTO reader VALUES(88,'lznr-jhaiec','blqyypnjqswdaquvoedrfojmjh',151,0);
INSERT INTO reader VALUES(89,'lznr-grhozm','zedjiriidptnhr',145,0);
INSERT INTO reader VALUES(90,'lznr-otk','tgfnstmhvvsmilsumdnrzllpu',131,0);
INSERT INTO reader VALUES(91,'plbyy-nhqj','nydvnvokitfdigqoscxfbgncd',199,0);
INSERT INTO reader VALUES(92,'plbyy-wnfe','cvqtsudluwjohqubthmlwfa',162,0);
INSERT INTO reader VALUES(93,'plbyy-adcs','amhrlnhahojesxv',149,0);
INSERT INTO reader VALUES(94,'plbyy-dfhpuj','komitpszhfosr',80,0);
INSERT INTO reader VALUES(95,'plbyy-kjtm','psxzkvthkgupjusmykajqjkljp',174,0);
INSERT INTO reader VALUES(96,'plbyy-oikbnytnyl','uzxatbdgunizgyxgs',200,0);
INSERT INTO reader VALUES(97,'plbyy-zhvb','qdrykaelpicfq',54,0);
INSERT INTO reader VALUES(98,'plbyy-jhaiec','orgwynuwxefveeuuvfj',114,0);
INSERT INTO reader VALUES(99,'plbyy-grhozm','rmqjmypofbqqehfrbhhpjaf',148,0);
INSERT INTO reader VALUES(100,'plbyy-otk','lvcjkvrejusm',86,0);
