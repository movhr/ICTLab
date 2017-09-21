'use strict';
var express = require("express"),
    app = express(),
    vhost = require("vhost"),
    http = require("http").createServer(app),
    cookieparser = require("cookie-parser"),
    //io = require("socket.io").listen(http),
    cors = require("cors"),
    api1 = require("./api1/api1"),
    api2 = require("./api2/api2"),
    api3 = require("./api3/api3"),
    userapi = require("./userlib/userlib_handler"),
    userviews = require("./views/user/user_views"),
    sensorviews = require("./views/sensor/sensor_views"),
    grafana = require("./grafanalib/grafanalib"),
    proxy = require("express-http-proxy");

// The following line fix CORS error when requesting apiX.localhost.
app.use(cors());

// Implement cookies
app.use(cookieparser());

app.set('view engine', 'pug')
   .set('views', __dirname + '/views')
   .set('customrootdir', __dirname);

app.use(vhost("api1.localhost", api1))
   .use(vhost("api2.localhost", api2))
   .use(vhost("api3.localhost", api3))
   .use("/api1", api1)
   .use("/api2", api2)
   .use("/api3", api3)
   .use("/user", userviews)
   .use("/sensor", sensorviews)
   .use("/grafana", proxy("http://localhost:3000/"))
   .use(userapi);

app.get("/", (req, res) => {
    res.render('index', {
        role: req.cookies['role'],
        message: 'Hello there!'
    });
});

http.listen(3001, () => {
    console.log("Listening on port 3001.");
});

module.exports = app;