const mongodb = require('mongodb');
const MongoClient = mongodb.MongoClient;
const url = require('../config/mongo').url;
let db;


exports.connect = function () {
  return new Promise((resolve, reject) => {
    MongoClient.connect(url, function (err, database) {
      if (err) reject(err);
      db = database;
      resolve();
    });
  });
}

exports.close = function () {
  if (db) db.close();
} 

exports.get = function () {
  return db
}

exports.list = function (collectionName, callback) {
  db.collection(collectionName).find().toArray(function (err, result) {
    console.log(err)
    if (err) throw err;
    callback(result);
  });
}

exports.insert = function (collectionName, data) {
  return new Promise((resolve, reject) => {
    db.collection(collectionName).insertOne(data, function (err, result) {
      if (err) return reject(err);
      resolve(result);
    });
  });
}


exports.updateOne = function (collectionName, query, newValues) {
  return new Promise((resolve, reject) => {
    db.collection(collectionName).updateOne(query, newValues, function (err, result) {
      if (err) return reject(err);
      resolve(result);
    });
  });
}

exports.delete = function (collectionName, query, callback) {
  db.collection(collectionName).deleteOne(query, function (err, result) {
    if (err) throw err;
    callback(result);
  });
}

exports.drop = function (collectionName) {
  return new Promise((resolve, reject) => {
    db.collection(collectionName).drop(function (err, result) {
      if (err) return reject(err);
      resolve(result);
    });
  });
}

exports.findWithQuery = function (collectionName, query, select = {}) {
  return new Promise((resolve, reject) => {
    db.collection(collectionName).find(query, select).toArray(function (err, result) {
      if (err) return reject(err);
      resolve(result);
    });
  });
}

exports.findOne = function (collectionName, query, select = {}) {
  return new Promise((resolve, reject) => {
    db.collection(collectionName).findOne(query, function(err, result) {
      if (err) return reject(err);
      resolve(result);
    });
  });
}

exports.findValueCounts = function (collectionName, columnName, max) {
  return new Promise((resolve, reject) => {
    db.collection(collectionName).aggregate([{$group : {"_id" : columnName, "count" : {$sum : 1}}}, 
    {$sort:{"count" : -1}}, {$limit : max}], 
    function(err, result) {
      if (err) return reject(err);
      resolve(result);
    });
  });
}