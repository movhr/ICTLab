'use strict';
var express = require("express");
var influxclient = require("../connectors/influx");
var mariaclient = require("../connectors/maria")
var bodyParser = require("body-parser");

var app = express();

app.get("/gethistorics", function (req, res) {

    function sendErr(code, msg) {
        res.status(code).send(msg);
        return false;
    }

    function sendDefaultErr(reason) {
        console.log(reason);
        return sendErr(500, "Something went wrong while accessing the database");
    }

    var datasetName = req.query.dataset;
    var dateStart = new Date(Number.parseInt(req.query.from));
    var dateEnd = new Date(Number.parseInt(req.query.to));

    var qryString = "SELECT timestamp, location, \"name\", type, value FROM " + datasetName +
        " WHERE time > '" + new Date(Number.parseInt(req.query.from)).toISOString() +
        "' AND time < '" + new Date(Number.parseInt(req.query.to)).toISOString() + '\'';


    if (!(datasetName && dateStart && dateEnd)) {
        return sendErr(400, "Invalid data");
    }

    var maria = mariaclient.client;
    maria.query("CALL SENSOR_GET_AS_ENTITY();", (err, rows) => {
        if (err)
            return sendDefaultErr();
        var ic = influxclient.reader;

        //Check if dataset exists
        ic.getMeasurements()
            .then(
                //on success
                function (result) {
                    var index = result.findIndex(function (val) {
                        return val === datasetName;
                    });
                    if (index < 0) {
                        return sendErr(400, "Invalid dataset name");
                    }

                    ic.queryRaw(qryString)
                        .then(
                            //on success

                            (result) =>
                            res.status(200).send({
                                entities: rows[0],
                                activity_log: result
                            }).end(),
                            //on error
                            sendDefaultErr
                        );
                },
                //on error
                sendDefaultErr
            );
    })
});

app.get("/getsimsample", function(req, res) {
    const path = "/home/user/Projects/ictlab/sample_historics_new.json";
    res.sendFile(path);
});

module.exports = app;
