var maria = require("../connectors/maria");
const PATH_INELIGABLE = "ineligable";

function render(res, url){
    res.render(url);
    return;
}

function requiresUserRole(role, cookies, urlPath, res){
    if(!cookies.role)
        return render(res, PATH_INELIGABLE);
    let accessToken = cookies['access_token'];
    if(!accessToken)
        return render(res, PATH_INELIGABLE);
    maria.MariaParameterizedQuery("SELECT `USER_GET_ROLE`(:cookie) as userrole;", {cookie:accessToken}, (result) =>{
    if(result.code)
        return render(res, PATH_INELIGABLE);
    else
        (role === result.userrole) ? res.render(urlPath): res.render(PATH_INELIGABLE);
    });
    
}

function requiresUserRoleCallback(role, cookies, success, res){
    if(!cookies.role)
        return render(res, PATH_INELIGABLE);
    let accessToken = cookies['access_token'];
    if(!accessToken)
        return render(res, PATH_INELIGABLE);
    maria.MariaParameterizedQuery("SELECT `USER_GET_ROLE`(:cookie) as userrole;", {cookie:accessToken}, (result) =>{
    if(result.userrole === role)
        success();
    else
        return render(res, PATH_INELIGABLE);
    });
}

module.exports.requiresUserRole = requiresUserRole;
module.exports.requiresUserRoleCallback = requiresUserRoleCallback;