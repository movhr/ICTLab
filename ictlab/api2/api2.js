'use strict'
var app = require("express")();
var bodyParser = require("body-parser");

var sensorlib = require("../sensorlib/sensorlib");
var sendErr = require("../error_handling/invalid_request").sendErr;

app.use(bodyParser.json()); // for parsing application/json
app.use(bodyParser.urlencoded({
    extended: true
})); // for parsing application/x-www-form-urlencoded

app.get("/getnodes", (req, res) => sensorlib.GetNodeNames(req, res))
    .get("/gettypes", (req, res) => sensorlib.GetSensorTypes(req, res))
    .get("/getinstances", (req, res) => sensorlib.GetInstances(res))
    .get("/verify", (req, res) => {
        var token = req.query.token;
        if (token.length === 7 && typeof (token) === 'string')
            sensorlib.Verify(token, res);
        else
            return sendErr(res);
    })
    .post("/register", (req, res) => {
        var device = req.body.device;
        var name = req.body.name;
        var type = req.body.type;
        var parent = req.body.parent;
        var locX = req.body.loc_x;
        var locY = req.body.loc_y;
        var locZ = req.body.loc_z;
        var desc = req.body.description;

        if (!(name && type && parent && locX && locY && locZ && desc))
            return sendErr(res);

        if (device === 'Node')
            sensorlib.RegisterNode(name, parent, locX, locY, locZ, desc, res);
        else if (device === 'Sensor')
            sensorlib.RegisterSensor(name, type, parent, locX, locY, locZ, desc, (mdbres) => mdbres.code ? res.send(mdbres) : res.send(mdbres[0].token));
        else
            return sendErr(res);

    })
    .post("/edit", (req, res) => {
        try{
        var sensorID = parseInt(req.body.sensorID);
        var nodeID = parseInt(req.body.nodeID);
        var newName = String(req.body.newName);
        var newEnabled = String(req.body.newEnabled);
        var newX = parseFloat(req.body.newX);
        var newY = parseFloat(req.body.newY);
        var newZ = parseFloat(req.body.newZ);
        var newDesc = String(req.body.newDesc);
        var newType = String(req.body.newType);
        }catch(err){
            res.send(400, "Error while parsing values").end();
            return;
        }
        sensorlib.Edit(sensorID, nodeID, newName, newEnabled,newX,newY,newZ,newDesc,newType, res);
    });

module.exports = app;