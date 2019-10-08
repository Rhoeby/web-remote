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
    imageRefreshRate: 1000,
    locationNameInput: "",
    itemToDelete: "",

  },
  computed: {
    battery: function(){
        //returns the correct icon based on battery percentage
        if (this.battery_percentage > 90) return "fas fa-battery-full"
        if (this.battery_percentage > 65) return "fas fa-battery-three-quarters"
        if (this.battery_percentage > 36) return "fas fa-battery-half"
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
    focusModal: function(){
      $('#locationName').focus()

    },
    saveNav: function(){
        var self=this
        $.get("/saveNavigation", {
            location: self.locationNameInput,
        }, function(){
          this.locationNameInput = ""
          this.timerBase = 0;
          this.mode = this.mode_enum.start
          this.loadData()
        })
    },
    discardNav: function(){
        $.get("/discardNavigation")
        this.timerBase = 0;
        this.mode = this.mode_enum.start
    },

    loadData: function(){
        console.log("loadData")
        var self = this
        $.get("/loadData/", function(data){
            //console.log(data)
            self.battery_percentage = data.battery_percentage
            self.past_runs = data.past_runs
            self.robot_name = data.robot_name
        })
    },
    previewVideo: function(run){
      previewSource = '/static/data/'+ run.name + '/video.mp4'
      htmlCode = '<video controls class="embed-responsive-item" id="preview_video">' +
      '<source src="' + previewSource + '" >' + 
      '</video>'
      $("#player").html(htmlCode)
    },
    deleteData: function(item){
      var self = this
      $.get("/deleteData", {
        name: item,
      }).then(function(){
        self.loadData()
      })
    },

  },
  beforeMount(){
    this.loadData()
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
