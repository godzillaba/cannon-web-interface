// defining websocket behavior

window.onload = function() {
    
    //socket = new WebSocket("ws://" + window.location.hostname + ":9000");
    socket = new WebSocket("ws://" + window.location.hostname + ":8888/websocket");

    socket.binaryType = "arraybuffer";
    
    socket.onopen = function() {
        console.log("Connected!");
        isopen = true;
    }
    
    socket.onmessage = function(e) {
        console.log("Text message received: " + e.data);
        messageObject = JSON.parse(e.data)
        if (messageObject.update) {
            if (messageObject.action == "fire_reload" && messageObject.info == "complete"){
                $("#space, #z").removeClass("btn_disabled")
            }
        }
    }
    
    socket.onclose = function(e) {
        console.log("Connection closed.");
        socket = null;
        isopen = false;
    }
};

// end defining websocket behavior

///////////////////////////

// key map

var keyMap = {
    38: {
        "character": "up",
        "pressed": false,
        "message": {
            "command": "stepper",
            "axis": "y",
            "direction": 1
        }
    },
    40: {
        "character": "down",
        "pressed": false,
        "message": {
            "command": "stepper",
            "axis": "y",
            "direction": 0
        }
    },
    37: {
        "character": "left",
        "pressed": false,
        "message": {
            "command": "stepper",
            "axis": "x",
            "direction": 0
        }
    },
    39: {
        "character": "right",
        "pressed": false,
        "message": {
            "command": "stepper",
            "axis": "x",
            "direction": 1
        }
    },
    32: {
        "character": "space",
        "pressed": false,
        "message": {
            "command": "fire"
        }
    },
    90: {
        "character": "z",
        "pressed": false,
        "message": {
            "command": "reload"
        }
    }
}

// end key map

///////////////////////////

// define button press and release functions

var actionButtonPressed = function (key) {
    
    var msg = null
    
    if ($("#" + key.character).hasClass("btn_disabled")){
        console.log('wait')
    } else {
        switch (key.character) {
            case "up":
            case "down":
            case "left":
            case "right":
                msg = key.message
                msg.start = true
                break;
            
            case "z":
            case "space":
                msg = key.message
                $("#z, #space").addClass("btn_disabled")
                break;

        }
        socket.send(JSON.stringify(msg))
    }
}

var actionButtonReleased = function (key) {
    
    var msg = null
    
    switch (key.character) {
        case "up":
        case "down":
        case "left":
        case "right":
            msg = key.message
            msg.start = false
            break;

    }
    if (msg){
        socket.send(JSON.stringify(msg))
    }
}

// end define button press and release functions

///////////////////////////

// math

function toRadians (angle) {
  return angle * (Math.PI / 180);
}


var P = {
    "barrelLength": 0.910,
    "projectileMass": 0.06,
    "pressure": 120.0,
    "theta": 45.0
}


var calculatePhysics = function () {
    var returnData = new Object();
    
    // find energy from pressure somehow (defining it in P for now...)
    returnData.energy = Math.round((0.2005*P.pressure - 0.3479)*100) / 100

    returnData.velocity = Math.round((Math.sqrt((2*P.barrelLength*returnData.energy)/P.projectileMass)) * 100) / 100

    returnData.airTime = Math.round((returnData.velocity * Math.sin(toRadians(P.theta)) / 4.9) * 100) / 100

    returnData.distance = Math.round((returnData.velocity * Math.cos(toRadians(P.theta)) * returnData.airTime) * 100) / 100


    $("#pressure").html(P.pressure)
    $("#theta").html(P.theta)
    
    $("#energy").html(returnData.energy)
    $("#velocity").html(returnData.velocity)
    $("#time").html(returnData.airTime)
    $("#predictedDistance").html(returnData.distance)


    return returnData
}

$(window).load(function(){
    calculatePhysics()
})

// end math


///////////////////////////


// button press and release capturing

$("html").keydown(function(e) {
    try {
        var key = keyMap[e.keyCode]

        if (!key.pressed) {
            actionButtonPressed(key)
        }

        key.pressed = true


        $("#" + key.character).css("opacity", 0.5)
    } 
    catch (E) { 
        if (E instanceof TypeError) {}
        else {
            throw E
        }
    }

})

$("html").keyup(function(e) {
    try {
        var key = keyMap[e.keyCode]

        key.pressed = false

        actionButtonReleased(key)

        $("#" + key.character).css("opacity", 1)
    } 
    catch (E) { 
        if (E instanceof TypeError) {}
        else {
            throw E
        }
    }
})

$(window).load(function(){
    var btns = $(".ui_btn")

    btns.mousedown(function(){
        actionButtonPressed(keyMap[$(this).data("key")])
    });

    btns.mouseup(function(){
        actionButtonReleased(keyMap[$(this).data("key")])
    })
})

// end button press and release capturing


///////////////////////////

// positioning miscellaneous elements
$(window).load(function() {
    $("#up").css("margin-left", $("#down").position().left + 5);
    var f = $("#feed")
    var uio = $("#userInputOutput")
    f.width(uio.offset().left - f.offset().left - 50)

    f.height($(window).height() - f.offset().top * 2)
})

// end positioning

