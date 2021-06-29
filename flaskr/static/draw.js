var canvas;
var context;
var clickX = new Array();
var clickY = new Array();
var clickDrag = new Array();
var paint = false;
var curColor = "#FF5733";

function drawCanvas() {
    canvas = document.getElementById('canvas');
    context = document.getElementById('canvas').getContext("2d");
    // context.lineWidth = 10;
    // context.strokeStyle = "#000000";
    // context.strokeRect(0, 67, 800, 733);
    $('#canvas').mousedown(function (e) {
        var mouseX = e.pageX - this.offsetLeft;
        var mouseY = e.pageY - this.offsetTop;

        paint = true;
        addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop);
        redraw();
    });
    $('#canvas').mousemove(function (e) {
        if (paint) {
            addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop, true);
            redraw();
        }
    });
    $('#canvas').mouseup(function (e) {
        paint = false;
    });
}

function addClick(x, y, dragging) {
    clickX.push(x);
    clickY.push(y);
    clickDrag.push(dragging);
}

function redraw() {
    context.clearRect(0, 0, context.canvas.width, context.canvas.height);
    context.strokeStyle = curColor;
    context.lineJoin = "round";
    context.lineWidth = 3;
    for (var i = 0; i < clickX.length; i++) {
        context.beginPath();
        if (clickDrag[i] && i) {
            context.moveTo(clickX[i - 1], clickY[i - 1]);
        } else {
            context.moveTo(clickX[i] - 1, clickY[i]);
        }
        context.lineTo(clickX[i], clickY[i]);
        context.closePath();
        context.stroke();
    }
    // context.lineWidth = 10;
    // context.strokeStyle = "#000000";
    // context.strokeRect(0, 67, 800, 733);
}

function save() {
    var image = new Image();
    var url = document.getElementById('url');
    image.id = "pic";
    image.src = canvas.toDataURL();
    url.value = image.src;
}
