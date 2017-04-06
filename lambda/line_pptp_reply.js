'use strict';

//
console.log("Start code!");

const https = require('https');
var AWS = require("aws-sdk");

AWS.config.update({region: "us-east-1",});
var docClient = new AWS.DynamoDB.DocumentClient();

let send = (data, callback) => {

  let body = JSON.stringify(data);

  let req = https.request({
    hostname: "api.line.me",
    port: 443,
    path: "/v2/bot/message/reply",
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Content-Length": Buffer.byteLength(body),
      "Authorization": "Bearer " + process.env.CHANNEL_ACCESS_TOKEN
    }
  });

  req.end(body, (err) => {
    err && console.log(err);
    callback(err);
  });
};

exports.handler = (event, context, callback) => {
  console.log("Start exports.handler!");
  console.log('EVENT:', JSON.stringify(event, null, 2));

  var event_data = JSON.parse(event.body);

  let result = event_data.events && event_data.events[0];
  if (result) {
    console.log("event true.");
    let content = event_data.events[0] || {};
    // content.type = ("follow","unfollow","message")
    switch (content.type){
        case "message":
            let message = {
                "replyToken":result.replyToken,
                "messages": [
                    {
                        "type": "text",
                        "text": ka[Math.floor(Math.random() * ka.length)]
                    }
                ]
            };
            console.log("call send with message ->" + message);
            send(message, () => {callback();});
            break;
        case "follow":
            console.log ("follow this user ->" + content.source.userId);
            set_friend(content.source.userId);
            var sticker = Math.floor(Math.random () * 430) + 1;
            let greeting = {
                "replyToken":result.replyToken,
                "messages": [
                    {
                        "type": "sticker",
                        "packageId": "1",
                        "stickerId": sticker
                    }
                ]
            };
            send(greeting, () => {callback();});
            break;
        case "unfollow":
            console.log ("unfollow this user ->" + content.source.userId);
            del_friend(content.source.userId);
            break;
    }
  } else {
    console.log("event false.");
    callback();
  }
};

function set_friend(userid){
    // not friend yet -> add
    console.log("start set friend"); //後で消す
    if(!is_friend(userid)){
    var params = gen_item_params(userid);
        console.log("Adding a new item...");
        docClient.put(params, function(err, data) {
            if (err) {
                console.error("Unable to add item. Error JSON:", JSON.stringify(err, null, 2));
            } else {
                console.log("Added item:", JSON.stringify(data, null, 2));
            }
        });
    } else {
        console.log("This user is already friend :)");
    }
    console.log("finish set friend"); //後で消す
    return;
}

function del_friend(userid){
    console.log("Attempting a conditional delete...");
    var params = gen_key_params(userid);
    docClient.delete(params, function(err, data) {
        if (err) {
            console.error("Unable to delete item. Error JSON:", JSON.stringify(err, null, 2));
        } else {
            console.log("DeleteItem succeeded:", JSON.stringify(data, null, 2));
        }
    });
    return;
}

function is_friend(userid){
    var params = gen_key_params(userid);
    docClient.get(params, function(err, data) {
        if (err) {
            console.error("Unable to read item. Error JSON:", JSON.stringify(err, null, 2));
            return false;
        } else {
            console.log("GetItem succeeded:", JSON.stringify(data, null, 2));
            return true;
        }
    });
}

function gen_key_params(userid){
    var params = {
        TableName: process.env.TABLE_USERS,
        Key:{
            "id": userid
        }
    };
    return params;
}

function gen_item_params(userid){
    var params = {
        TableName: process.env.TABLE_USERS,
        Item:{
            "id": userid
        }
    };
    return params;
}

var ka = [
  "おこった？", "あ”あ”？", "あ”ァ”？","今日も1日がんばるぞい！","アンチ〜♪",
  "信者〜♪","さてはアンチだなオメー", "ほう だんまりか", "きゅっ きゅっ", "もしもし",
  "ポリスメン？", "バーカ！！！", "なんだ…？ テメェ…", "竹書房ゥァア”ーッ", "つっこむぞ つかまれッ！",
  "あー そーゆーことね", "自己顕示欲〜", "いやよくみたらクソむかつく", "どこいきやがった…", "ファーイwww",

  "https://youtu.be/BBgghnQF6E4"
];
