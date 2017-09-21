var app = require("express")();
var mariaconnector = require("../connectors/maria").client;
var bodyParser = require("body-parser");
var invalidRequest = require("../error_handling/invalid_request");

app.use(bodyParser.json()); // for parsing application/json
app.use(bodyParser.urlencoded({
    extended: true
})); // for parsing application/x-www-form-urlencoded

app.post("/login", (req, res) => {
    var sendErr = () => invalidRequest.sendErr(res);

    var email = req.body.email;
    var password = req.body.password;

    if (!(email && password)) {
        return sendErr(res);
    }

    //TODO: Add rows for login sessions in database table User
    mariaconnector.query("SELECT `USER_LOGIN`(:email,:password) as accesstoken;", {
        email: email,
        password: password
    }, (err, rows) => {
        if (err) {
            return sendErr(err.message);
        }else {
            let accesstoken = rows[0].accesstoken
            mariaconnector.query("SELECT `USER_GET_ROLE`(:at) as role", {at:accesstoken}, (err,resp) => {
                if(err)
                    return sendErr(err.message);
                else{
                    res.status(200)
                       .clearCookie("access_token")
                       .clearCookie("role")
                       .cookie("access_token", accesstoken)
                       .cookie("role", resp[0].role)
                       .send()
                       .end();
                }
            });
            
        }
    });
});

module.exports = app;