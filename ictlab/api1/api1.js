'use strict';
var app = require("express")();
var bodyParser = require("body-parser");
var pairwiseArray = require("../lib/pairwiseArray");
var influxconnector = require("../connectors/influx");
var mariaconnector = require("../connectors/maria");
var invalidRequest = require("../error_handling/invalid_request");

app.use(bodyParser.json()); // for parsing application/json
app.use(bodyParser.urlencoded({
    extended: true
})); // for parsing application/x-www-form-urlencoded

app.post("/upload", function (req, res) {
    var sendErr = () => invalidRequest.sendErr(res); 

    var parseInput = (_at, _date, _value, _name, _loc, _type) => {
        return {
            tags: {
                "sensor": _at,
                "name": _name,
                "location": _loc,
                "type": _type,
                "timestamp": Date.parse(_date)
            },
            fields: {
                "value": parseFloat(_value)
            }
        }
    }

    var at = req.body.access_token;
    var dates = req.body.labels;
    var values = req.body.data;
    var arrays = false;

    //Check for data validity
    if (!(at && dates && values)) {
        return sendErr(res);
    }
    if (Array.isArray(dates) && Array.isArray(values)) {
        if (dates.length != values.length)
            return sendErr(res);
        arrays = true;
    } else if (Array.isArray(dates) || Array.isArray(values)) {
        return sendErr(res);
    }

    //check validity of AT in MariaSQL
    //if not valid, exec same func as above
    let client = mariaconnector.client;
    client.query("CALL SENSOR_GET(:at)", {
        at: at
    }, (err, rows) => {
        if (err) {
            return sendErr(res);
        }

        var sensor = rows[0][0];
        if (sensor.Enabled !== "1") {
            res.status(200).send().end();
            return;
        }

        //parse dates and values
        var points = null;
        if (!arrays) {
            points = [parseInput(at, dates, values, sensor.Name, sensor.Location, sensor.Type)];
        } else {
            points = pairwiseArray(dates, values, (d, v) => parseInput(at, d, v, sensor.Name, sensor.Location, sensor.Type));
        }

        var lastValue = arrays ? values[values.length-1] : values;
        client.query("CALL SENSOR_UPDATE(:at, :lv)", {
            lv: lastValue,
            at: at
        }, (err) => {
            if (err) {
                return sendErr(res);
            }

            //Write to tsdb server
            let ic = influxconnector.writer;
            ic.writeMeasurement("sensor_data", points).then(() => {
                res.status(200).send().end();
                client.end();
            }).catch((err) => {
                console.log(err);
                res.status(500).send().end();
                client.end();
            });
        })
    });
});

module.exports = app;