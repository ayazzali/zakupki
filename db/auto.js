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
	'products.okdp_code': 3410010,
	'products.sum': {
		$gt: 1000000
	}
}

group_query = {
	reduce: function (current, result) {
		result.total += current.price;
	},
	cond: { 'products.okdp_code': 3410010 },
	initial: { total: 0.0 }
};

var res = db.contracts.group(group_query);

printjson(res[0].total)

// var res = db.products.find(n_query).toArray();

// for (i = 0; i < res.length; i++) {
// 	printjson(res[i]);
// }