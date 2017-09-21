function sendErr(response, msg) {
    response.status(400).send(msg || "Invalid data").end();
    return false;
}

module.exports.sendErr = sendErr;