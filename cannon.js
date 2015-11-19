
var keyMap = {
    38: {
        "character": "up",
        "pressed": false
    },
    40: {
        "character": "down",
        "pressed": false
    },
    37: {
        "character": "left",
        "pressed": false
    },
    39: {
        "character": "right",
        "pressed": false
    },
    32: {
        "character": "space",
        "pressed": false
    },
    82: {
        "character": "r",
        "pressed": false
    }
}


var actionButtonPressed = function (arg) {
    console.log(arg + " DOWN")
}

var actionButtonReleased = function (arg) {
    console.log(arg + " UP")
}


$("html").keydown(function(e) {
    try {
        var key = keyMap[e.keyCode]

        if (!key.pressed) {
            actionButtonPressed(key.character)
        }

        key.pressed = true


        $("#" + key.character).css("opacity", .5)
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

        actionButtonReleased(key.character)

        $("#" + key.character).css("opacity", 1)
    } 
    catch (E) { 
        if (E instanceof TypeError) {}
        else {
            throw E
        }
    }
})

function toRadians (angle) {
  return angle * (Math.PI / 180);
}


var P = {
    "barrelLength": 0.910,
    "projectileMass": 0.10,
    "pressure": 50.0,
    "theta": 37.8,
    "force": 26
}


var calculatePhysics = function () {
    var returnData = new Object();
    
    // find force from pressure somehow (defining it in P for now...)

    returnData.velocity = Math.round((Math.sqrt((2*P.barrelLength*P.force)/P.projectileMass)) * 100) / 100

    returnData.airTime = Math.round((returnData.velocity * Math.sin(toRadians(P.theta)) / 4.9) * 100) / 100

    returnData.distance = Math.round((returnData.velocity * Math.cos(toRadians(P.theta)) * returnData.airTime) * 100) / 100


    $("#pressure").html(P.pressure)
    $("#theta").html(P.theta)
    $("#force").html(P.force)


    $("#velocity").html(returnData.velocity)
    $("#time").html(returnData.airTime)
    $("#predictedDistance").html(returnData.distance)


    return returnData
}

$(window).load(function(){
    calculatePhysics()
})


$(window).load(function(){
    var btns = $(".ui_btn")

    btns.mousedown(function(){
        actionButtonPressed($(this).prop("id"))
    });

    btns.mouseup(function(){
        actionButtonReleased($(this).prop("id"))
    })
})


$(window).load(function() {
    $("#up").css("margin-left", $("#down").position().left + 5);
    var f = $("#feed")
    var uio = $("#userInputOutput")
    f.width(uio.offset().left - f.offset().left - 50)

    f.height($(window).height() - f.offset().top * 2)
})



