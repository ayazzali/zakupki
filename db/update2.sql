create index ind_notifications_publish_date on notifications (publish_date);

alter table notifications
	add column max_price numeric(36, 4);