psql -U postgres -f ../sql/init_postgres.sql &>> ../logs/zakupki.log
psql -U roveo -d zakupki -f ../sql/setup_roveo.sql &>> ../logs/zakupki.log