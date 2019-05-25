const database = require('../utils/db-connection');

exports.getSession = async function (sessId) {
    
    // const { spawn } = require('child_process');
    // const py = spawn("python3", ["app_only_python.py", sessId]);
    
    // return new Promise((resolve, reject) =>{
    //     py.stdout.on("data", data =>{
    //         resolve(data.toString());
    //     })
    //     py.stderr.on("data", reject)
    // });
    
    sessionInfoPred = await database.findWithQuery('processed-logs', { session: sessId });
    sessionInfoTrue = await database.findOne('logs', { session: sessId });
    
    sessionInfo = {
        'true': sessionInfoTrue.eventid,
        'pred': sessionInfoPred
    };
    return sessionInfo;
}    

exports.getValueCounts = function (colName, max) {
    return database.findValueCounts('logs', colName, max).
    then(records => {
        return records.map(({ _id, count }) => {
            return { _id, count };
        });
    });
}

