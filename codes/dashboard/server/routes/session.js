var express = require('express');
var router = express.Router();

const {
    parseQueryString,
    parseHexToString
} = require('../utils/common-middleware');
  
const wrap = fn => (...args) => fn(...args).catch(args[2]);

const {
  getSessionSeq,
  getValueCounts
} = require('../controllers/session');

router.get('/session/:sessId', wrap(getSessionSeq), parseHexToString);
router.get('/common', parseQueryString, wrap(getValueCounts), parseHexToString);

module.exports = router;
