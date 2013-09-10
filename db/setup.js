db = new Mongo().getDB('admin');
db.addUser({
	user: 'roveo', // admin
	pwd: 'Ml3o5CHb',
	roles: ['readWriteAnyDatabase', 'userAdminAnyDatabase', 'dbAdminAnyDatabase']
});

db = new Mongo().getDB('zakupki');
db.addUser({
	user: 'update', // script writer
	pwd: 'raz dva tri putin uhodi',
	roles: ['readWrite']
});
db.addUser({
	user: 'remoteReader', // remote reader
	pwd: 'zhaba na trube',
	roles: ['read']
});