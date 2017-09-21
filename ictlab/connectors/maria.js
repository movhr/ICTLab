var mariaclient = require("mariasql");

var client = new mariaclient({
    host: "127.0.0.1",
    user: "root",//"webclient",
    password: "masterkey",//"YoullNeverGuessThis",
    db: "chibb"
});

var MariaQuery = (str, res) =>
    client.query(str, (err, rows) => {
        if (err) {
            if (typeof (res) === 'function')
                return res(err);
            else if (res) {
                res.status(500).send(err).end();
                return;
            } else
                throw err;
        }
        if (typeof (res) === 'function')
            return res(rows[0]);
        else if (res) {
            res.status(200).send(rows[0]).end();
            return;
        } else
            return rows[0];
    });

var MariaParameterizedQuery = (str, dict, res) =>
    MariaQuery(client.prepare(str)(dict), res);


module.exports.client = client;
module.exports.MariaParameterizedQuery = MariaParameterizedQuery;
module.exports.MariaQuery = MariaQuery;