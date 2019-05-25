var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

const database = require('./utils/db-connection');

const { 
  successResponse, 
  errorResponse,
  allowCrosAccess
   } = require('./utils/middlewares');

const {
  sessionRouter
} = require('./routes');

var app = express();


app.use(allowCrosAccess);

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());

app.use('/session', sessionRouter);

app.use(successResponse);
app.use(function(req, res, next) {
    next(createError(404));
});
app.use(errorResponse);

app.use(function(req, res, next) {
  next(createError(404));
});

app.use(function(err, req, res, next) {
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  res.status(err.status || 500);
  res.render('error');
});

database.connect()
    .catch(err => console.log('Error in Mongo Connection creation.'));

module.exports = app;
