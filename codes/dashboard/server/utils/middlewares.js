exports.successResponse = function (req, res, next) {

	if (!res.locals.data) return next();
	res.json({
		data: res.locals.data,
		error: null
	});
}


exports.errorResponse = function (err, req, res, next) {

	res.status(err.status || 500).json({
		data: null,
		error: {
			message: err.message
		}
	});
}

exports.allowCrosAccess = function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization");
  if (req.method == "OPTIONS") {
    res.end();
  } else {
    next();
  }
}