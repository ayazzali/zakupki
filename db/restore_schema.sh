psql -U roveo -d zakupki -c "drop table notifications cascade;"
psql -U roveo -d zakupki < schema.dump