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

truncate table notifications;

alter table notifications
	drop column placer_name,
	drop column last_name,
	drop column first_name,
	drop column middle_name,
	drop column post_address,
	drop column email,
	drop column phone,
	drop column placer_regnum;

alter table notifications
	add column placer_reg_num bigint;

create table products (
	code int,
	parent_code int,
	product_name text,

	constraint products_pk primary key (code)
);