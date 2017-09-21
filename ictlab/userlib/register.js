'use strict'
var app = require("express")();
var mariaconnector = require("../connectors/maria").client;
var bodyParser = require("body-parser");
var invalidRequest = require("../error_handling/invalid_request");

app.use(bodyParser.json()); // for parsing application/json
app.use(bodyParser.urlencoded({
    extended: true
})); // for parsing application/x-www-form-urlencoded

app.post("/register", (req, res) => {
    var sendErr = (msg) => invalidRequest.sendErr(res, msg);

    var email = req.body.email;
    var password = req.body.password;
    var role = req.body.role;

    if (!(role && email && password)) {
        return sendErr(res);
    }

    //Insert user to database
    mariaconnector.query("CALL USER_INSERT(:email, :password, :role);", {
        email: email,
        password: password,
        role: role
    }, (err) => {
        if (err) {
            return sendErr(err.message);
        }

        res.status(200).send().end();
    });
});
module.exports = app;