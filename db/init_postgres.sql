create role admin with nologin superuser createdb createrole replication;
grant all privileges on database postgres to admin;
grant all privileges on schema public to admin;

create role roveo with login password 'test' in role admin;
create database zakupki;
grant all privileges on database zakupki to admin;
