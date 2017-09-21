var app = require("express")();
var register = require("./register");
var login = require("./login");

app.use("/userapi",register, login);

module.exports = app;