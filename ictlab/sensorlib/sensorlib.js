var mariaconnector = require("../connectors/maria");
var randomString = require("../lib/randomString").randomAsciiString;
var sendErr =require("../error_handling/invalid_request").sendErr;

var MariaParameterizedQuery = mariaconnector.MariaParameterizedQuery;
var MariaQuery = mariaconnector.MariaQuery;

var GetNodeNames = (req, res) => MariaQuery("CALL NODE_GETALL_NAME();", res);
var GetSensorTypes = (req, res) => MariaQuery("CALL SENSOR_TYPE_GETALL_DESCRIPTION();", res);
var GetInstances = (response) => MariaQuery("CALL INSTANCE_GET_ALL();", response);

var RegisterSensor = (name, type, parent, locX, locY, locZ, desc, response) => {
    let randString = randomString(7);
    MariaParameterizedQuery("CALL SENSOR_REGISTER(:token, :name, :type, :parent, :locx, :locy, :locz, :desc);", {
            token: randString,
            name: name,
            type: type,
            parent: parent,
            locx: locX,
            locy: locY,
            locz: locZ,
            desc: desc
        }, response);
    }

var RegisterNode = (name, parent, locX, locY, locZ, desc, response) =>
    MariaParameterizedQuery("CALL NODE_REGISTER(:name, :parent, :locx, locy, :locz, :desc);", {
            name: name,
            parent: parent,
            locx: locX,
            locy: locY,
            locz: locZ,
            desc: desc
        },response);


var Verify = (token, response) =>
    MariaParameterizedQuery("CALL SENSOR_VERIFY(:token);", {
            token: token
        }, response);


function Edit(sensorID, nodeID, name, enabled, x, y, z, desc, type, response) {
    const qry = "CALL INSTANCE_EDIT(:sensorID, :nodeID, :newName, :newEnabled, :newX, :newY, :newZ, :newDesc, :newType);";
    MariaParameterizedQuery(qry, {sensorID: sensorID, nodeID:nodeID, newName:name, newEnabled:enabled,newX:x,newY:y,newZ:z, newDesc:desc,newType:type}, response);
}

function Delete(isNode, sensorID, response){
    MariaParameterizedQuery("CALL INSTANCE_DELETE(:instanceID,:instanceType)", {instanceID: sensorID, instanceType: isNode ? "Node" : "Sensor"}, response);
}

module.exports.GetNodeNames = GetNodeNames;
module.exports.GetSensorTypes = GetSensorTypes;
module.exports.GetInstances = GetInstances;
module.exports.RegisterSensor = RegisterSensor;
module.exports.RegisterNode = RegisterNode;
module.exports.Verify = Verify;
module.exports.Edit = Edit;
module.exports.Delete = Delete;
