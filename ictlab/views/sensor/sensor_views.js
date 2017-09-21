var express = require("express");
var cp = require("cookie-parser");
var requiresUserRole = require("../../lib/cookieVerification").requiresUserRole;
var router = express.Router();
router.use(cp());

router.get("/register", (req, res) => 
    requiresUserRole('Sensor Admin', req.cookies,"sensor/register",res));
router.get("/edit", (req, res) => 
    requiresUserRole('Sensor Admin', req.cookies,"sensor/edit",res));

module.exports = router;