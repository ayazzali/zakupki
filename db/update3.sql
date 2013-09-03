create table organizations (
	reg_num bigint,
	short_name text,
	full_name text,
	okato character(11),
	zip int,
	postal_address text,
	email text,
	phone character(32),
	fax text,
	last_name text,
	first_name text,
	middle_name text,
	inn character(10),
	actual boolean,

	constraint organizations_pk primary key (reg_num)
);

create table products (
	code int,
	parent_code int,
	product_name text,

	constraint products_pk primary key (code)
);

drop table notifications;

set role admin;
create extension hstore;

create table notifications (
	id bigint default nextval('notifications_pk'),
	folder_name character(64),
	hlevel smallint not null,
	hparent bigint null,
	dict hstore not null,

	constraint pk_notification_id primary key (id)
)