const _ = require('underscore');

exports.parseQueryString = function(req, res, next) {
	if (_.isEmpty(req.query)) return next();
	for (let param in req.query) {
		req.query[param] = (Number(req.query[param]) || req.query[param]);
	}
	next();
}

exports.parseHexToString = function (req, res, next) {
	if (!res.locals.data) return next();
	next();
}