var app = require("express")();
var proxy = require("express-http-proxy");
var cookieparser = require("cookie-parser");
var requiresUserRoleCallback = require("../lib/cookieVerification").requiresUserRoleCallback;

app.use(cookieparser());
app.use("/", (req, res) => requiresUserRoleCallback('Data Scientist', req.cookies, () => proxy("http://localhost:3001"), res));

module.exports=app;