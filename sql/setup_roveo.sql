create sequence notifications_pk;

create table notifications (
	id bigint default nextval('notifications_pk'),
	rec_id bigint not null,
	notification_number character(19) not null,
	notification_type character(6),
	version_number int,
	create_date timestamp,
	publish_date timestamp,
	placer_regnum character(11),
	placer_name text,
	order_name text,
	last_name text,
	first_name text,
	middle_name text,
	post_address text,
	email text,
	phone text,
	href text,
	print_form text,
	folder_name character(64),

	constraint pk_notification_id primary key (id)
)