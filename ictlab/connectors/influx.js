var influx = require("influx");

var writer = new influx.InfluxDB({
    host: 'localhost',
    database: 'sensor_uploads',
    username: "Writer",
    password: "RETIRW"
});

var reader = new influx.InfluxDB({
    host: 'localhost',
    database: 'sensor_uploads',
    username: "Reader",
    password: "REDAER"
});

module.exports.writer = writer;
module.exports.reader = reader;