const {
    sessionService 
} = require('../services');
  
exports.getSessionSeq = async (req, res, next) => {

    const { sessId } = req.params;
    
    const sessionSeq = await sessionService.getSession(sessId);
    console.log('Returned Data: ', sessionSeq);
    res.locals.data = sessionSeq;
    
    next();
}

exports.getValueCounts = async (req, res, next) => {
    const max = req.query.max;
    const col = '$'+req.query.col;
    const valueCount = await sessionService.getValueCounts(col, max);
    res.locals.data = valueCount;
    next();
}