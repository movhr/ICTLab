'use strict';
module.exports = function (firstArray, secondArray, mapCallback) {
        var newArr = new Array(Math.min(firstArray.length, secondArray.length));
        for (var i = 0; i < newArr.length; i++) {
            newArr[i] = mapCallback(firstArray[i], secondArray[i]);
        }
        return newArr;
}