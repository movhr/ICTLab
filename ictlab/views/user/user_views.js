var express = require("express");
var router = express.Router();

router.get("/login", (req, res) => res.render("user/login"))
.get("/register", (req, res) => res.render("user/register"));

module.exports = router;