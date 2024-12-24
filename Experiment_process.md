### 1 Deploying Databases

The experiment of OpenGebhard is meant to compare several crucial performance aspects between two database ststems ,OpenGauss and Postgresql.

For the sake of equality ,the test is all done on a Huawei ECS. 

First ,the user should do as `HuaweiECS_OpenGauss.pdf` in order to **build OpenGauss on a Huawei ECS**.

Then ,the user should do as [The link](https://blog.csdn.net/m0_74824496/article/details/144252316) taught ,in order to **build Postgresql on a Huawei ECS**.

After both Databases are deployed successfully ,the user can start the experiment

### 2 Doing Experiment

First ,go to your root directory and **use git clone to download the codes**

Then ,go to `/OpenGebhard/code` and run `main.py` with **different system arguments**

* If you run with `python main.py write 100 200 300`

  The program will genarate a dataset of $100^2=10000$ people ,$200$ books and $300*10=3000$​​ transactions.

  You can choose argument numbers as you need

  The SQL scripts will be stored in `/OpenGebhard/SQLs`

* If you run with `python main.py exp_pg 100 3`

  The program will monitor the performance aspects for $100$ seconds ,and store it as the data of the **third experiment** of **postgresql**

* If you run with `python main.py exp_gs 200 5`

  The program will monitor the performance aspects for $200$ seconds ,and store it as the data of the **fifth experiment** of **OpenGauss**

* If you run with `python main.py paint`

  The program will paint out the result charts.

* **Caution : Make sure you have done 9 experiments (1-9) for both databases ,or this painting step won't work**

While running the **exp** steps ,of course you need to **run the sql scripts**.

In order to have the running sum time ,it is recommended to run them as down :

* For insert experiment :

  * On Postgresql :

    run `su postgres` (or username you created)

    then run `time /usr/local/postgresql/bin/psql -U postgres -d postgres -f /OpenGebhard/code/SQLs/test_inpg.sql`

  * On OpenGauss :

    run `su omm`(or username you created)

    then run ` gsql -p 26000 -d postgres -f /OpenGebhard/code/SQLs/test_ings.sql`

* For transaction experiment :

  * On both databases :

    do insertion as in the insert experiment first

    then run ` gsql -p 26000 -d postgres -f /OpenGebhard/code/SQLs/test_deal.sql`