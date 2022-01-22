'use strict';

// console.log("Start code!");

const https = require('https');
var AWS = require("aws-sdk");

AWS.config.update({region: "us-east-1",});
var docClient = new AWS.DynamoDB.DocumentClient();

var message = {};
var params = {};

let send = (data, callback) => {
  console.log("let send Start!");
  let body = JSON.stringify(data);

  let req = https.request({
    hostname: "api.line.me",
    port: 443,
    path: "/v2/bot/message/multicast",
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Content-Length": Buffer.byteLength(body),
      "Authorization": "Bearer " + process.env.CHANNEL_ACCESS_TOKEN
    }
  });

    console.log("This is req ->");
    console.log(req);
  req.end(body, (err) => {
    err && console.log(err);
    callback(err);
  });
  console.log("let send End!");
};

exports.handler = (event, context, callback) => {
    console.log("Start Handler!");
    console.log('EVENT:', JSON.stringify(event, null, 2));

    console.log("1. Generate Message Template");

    let content = event.Records[0];
    console.log("content ->");
    console.log(content);

    let month = content.dynamodb.NewImage.month.N;
    let day = content.dynamodb.NewImage.day.N;
    let sayThis = "ポプテピピック最新[" + month + "-" + day + "]が公開されたよ！";
    let url = "http://mangalifewin.takeshobo.co.jp/rensai/popute2/popute2-014/" + content.dynamodb.NewImage.serial.N;

    message = genNotification(sayThis, url);
    console.log("This is message ->");
    console.log(message);

    console.log("2. Scan User and multicast message");

    params = gen_scan_params();

    sendMessage4Scan(params,
        () => {send(message,
            () => {callback();});
        }
    );
};

function sendMessage4Scan(params,sendMethod){
    docClient.scan(params, (err, data) => onScan(err, data, sendMethod));
}


function genNotification(sayThis, url){
    console.log("gen notify"); //後で消す
    message = {
        "to":[],
        "messages": [
          {
            "type": "text",
            "text": sayThis
          },
          {
            "type": "text",
            "text": url
          }
        ]
    };
    return message;
}

function gen_scan_params(){
    params = {
        TableName: process.env.TABLE_USERS,
        ProjectionExpression: "id"
    };
    return params;
}

function onScan(err, data, sendMethod) {
    console.log("onScan start");//後で消す
    if (err) {
        console.error("Unable to scan the table. Error JSON:", JSON.stringify(err, null, 2));
    } else {
        console.log("onScan succeeded.");
        data.Items.forEach(function(user) {
            message.to.push(user.id);
        });
        console.log("This is message after Scan ->");
        console.log(message); // 後で消す

        // continue scanning if we have more movies, because
        // scan can retrieve a maximum of 1MB of data
        if (typeof data.LastEvaluatedKey != "undefined") {
            console.log("Scanning for more...");
            params.ExclusiveStartKey = data.LastEvaluatedKey;
            docClient.scan(params, onScan);
        }
        sendMethod();
    }
}
