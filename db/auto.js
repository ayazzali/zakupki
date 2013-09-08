db = new Mongo().getDB('zakupki');

r_query = {
	'name': {
		$regex: '.+легков.+автомобил.+',
		$options: 'i'
	}
}

n_query = {
	'_id': 3410010
}

a_query = {
	'products.okdp_code': 3410010
	// 'order_name': {
	// 	$regex: '.+chevrolet.+',
	// 	$options: 'i'
	// }
}

var res = db.contracts.find(a_query).toArray()

// print(res)

// var res = db.products.find(n_query).toArray();

for (i = 0; i < res.length; i++) {
	printjson(res[i]);
}