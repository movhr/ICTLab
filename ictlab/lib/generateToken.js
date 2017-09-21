var randomString = require("./randomString").randomString;

module.exports = function generateRegisterToken(length1,length2){
    var firstpart = randomString(length1, "ABCDEFGHIJKLMNOPQRSTUVWXYZ");
    var secondpart = randomString(length2, "1234567890");
    var token = firstpart + "-" + secondpart;
    return token;
}