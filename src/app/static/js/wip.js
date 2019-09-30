var app = new Vue({
  el: '#app',
  delimiters: ['${', '}'],
  data: {
    runningTimer: 0,
    battery_percentage: null,
    robot_name: null,
    mapImg: "/latestMap.jpg",
    mode_enum: {
        start: 0,
        run: 1,
        pause: 2,
    },
    mode: 0,
    past_runs: [],
    timerBase: 0,
    timerStarted: null,
    // JJ
    //imageRefreshRate: 5000,
    imageRefreshRate: 1000,
    locationNameInput: "",

  },
  computed: {
    battery: function(){
        //returns the correct icon based on battery percentage
        if (this.battery_percentage > 90) return "fas fa-battery-full"
        if (this.battery_percentage > 65) return "fas fa-battery-three-quarters"
        if (this.battery_percentage > 32) return "fas fa-battery-half"
        if (this.battery_percentage > 10) return "fas fa-battery-quarter"
        return "fas fa-battery-empty"
    },
  },
  created: function(){
    var self = this
    setInterval(function(){
        self.mapImg = "/latestMap.jpg?" + Date.now()
    }, self.imageRefreshRate)
  },
  methods: {
    startNav: function(){
        $.get("/startNavigation")
        var self = this
        this.timerStarted = Date.now()
        this.mode = this.mode_enum.run
        var updateTimer = function() {
            self.runningTimer = msToTime(self.timerBase + Date.now() - self.timerStarted)
            setTimeout(()=>{
                if (self.timerStarted) updateTimer()
            }, 250)
        }
        updateTimer()
    },
    pauseNav: function(){
        $.get("/pauseNavigation")
        this.timerBase = this.timerBase + Date.now() - this.timerStarted
        this.timerStarted = null
        this.mode = this.mode_enum.pause
    },
    saveNav: function(){
        var self=this
        $.get("/saveNavigation", {
            location: self.locationNameInput,
        })
        this.locationNameInput = ""
        this.timerBase = 0;
        this.mode = this.mode_enum.start
    },
    discardNav: function(){
        $.get("/discardNavigation")
        this.timerBase = 0;
        this.mode = this.mode_enum.start
    },

    setup: function(){
        console.log("setup")
        var self = this
        $.get("/loadData/", function(data){
            console.log(data)
            self.battery_percentage = data.battery_percentage
            self.past_runs = data.past_runs
            self.robot_name = data.robot_name
        })
    }

  },
  beforeMount(){
    this.setup()
  }
})

function msToTime(s) {
  var ms = s % 1000;
  s = (s - ms) / 1000;
  var secs = s % 60;
  s = (s - secs) / 60;
  var mins = s % 60;
  var hrs = (s - mins) / 60;
  if (hrs < 10) hrs = "0" + hrs
  if (mins < 10) mins = "0" + mins
  if (secs < 10) secs = '0' + secs

  return hrs + ':' + mins + ':' + secs
}