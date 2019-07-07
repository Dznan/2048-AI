var sleep = async (duration) => {
    return new Promise((resolve, reject) => {
        setTimeout(resolve, duration);
    });
};

var stopAuto = true;

function AIManager() {
    this.events = {};
    this.listen();
  }
  
  AIManager.prototype.on = function (event, callback) {
    if (!this.events[event]) {
      this.events[event] = [];
    }
    this.events[event].push(callback);
  };
  
  AIManager.prototype.emit = function (event, data) {
    var callbacks = this.events[event];
    if (callbacks) {
      callbacks.forEach(function (callback) {
        callback(data);
      });
    }
  };
  
  AIManager.prototype.listen = function () {
    var self = this;

    // // Respond to button presses
    this.bindButtonPress(".nextstep-button", this.nextstep);
    this.bindButtonPress(".autoplay-button", this.autoplay);
    // this.bindButtonPress(".keep-playing-button", this.keepPlaying);
  
    // if (Math.max(absDx, absDy) > 10) {
    // // (right : left) : (down : up)
    // self.emit("move", absDx > absDy ? (dx > 0 ? 1 : 3) : (dy > 0 ? 2 : 0));
    // }
  };
  
  AIManager.prototype.nextstep = async function (event) {
    event.preventDefault();
    var self = this;
    if(game.isGameTerminated()) return;
    let grid = game.grid.to_json();
    var postData = new URLSearchParams({
        "grid": JSON.stringify(grid),
    });
    await fetch("/api/nextstep", {
        method: "POST",
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: postData
    })
    .then(Response => Response.json())
    .then(res => {
        let actionList = {
            "U" : 0,
            "L" : 1,
            "D" : 2,
            "R" : 3
        };
        self.emit("move", actionList[res.action]);
    });
  };

  AIManager.prototype.autoplay = async function (event) {
    event.preventDefault();
    var self = this;
    stopAuto = !stopAuto;
    if (stopAuto) 
        document.querySelector(".autoplay-button").innerHTML = "Auto Play";
    else
        document.querySelector(".autoplay-button").innerHTML = "Stop";
    if (stopAuto) return; 
    while(!game.isGameTerminated()) {
        if (stopAuto) break;
        self.nextstep(event);
        await sleep(100);
    }
    if (!stopAuto) {
      stopAuto = !stopAuto;
      document.querySelector(".autoplay-button").innerHTML = "Auto Play";
    }
  };
  
  AIManager.prototype.bindButtonPress = function (selector, fn) {
    var button = document.querySelector(selector);
    button.addEventListener("click", fn.bind(this));
    button.addEventListener(this.eventTouchend, fn.bind(this));
  };
  