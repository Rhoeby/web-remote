var app = new Vue({
  el: '#app',
  delimiters: ['${', '}'],
  data: {
    runningTimer: 0,
    battery_percentage: null,
    robot_name: null,
    mapImg: "/latestMap.jpg",
    mode_enum: {
        loading: 0,
        start: 1,
        run: 2,
        pause: 3,
        end: 4,
    },
    mode: -1,
    past_runs: [],
    timerBase: 0,
    timerStarted: null,
    refreshRunData: false,
    imageRefreshRate: 1000,
    locationNameInput: "",
    itemToDelete: "",
    loading_msg: "",

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
        this.refreshRunData = true;
        this.mode = this.mode_enum.loading
        //wait a second for data to propigate before reloading
        setTimeout(function(){
          updateRunInfo(this)
        }, 150)
    },
    resumeNav: function(){
      $.get("/resumeNavigation")
      this.timerStarted = Date.now()
      this.mode = this.mode_enum.run
      updateRunInfo(this)
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
        updateRunInfo(this)
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

function updateRunInfo (self){
  $.get("/navigationStatus", function(data){
    console.log(data)
    if (self.mode == -1){
      console.log(data.state)
      self.mode = self.mode_enum[data.state]
      self.timerBase = data.deltaTime
      self.runningTimer = msToTime(self.timerBase)
    }
    self.timerBase = data.deltaTime
    if (self.mode == self.mode_enum.run){
      self.runningTimer = msToTime(self.timerBase)
      if(data.loading){
        self.mode = self.mode_enum.loading
      }
      else{
        self.mode = self.mode_enum.run
      }
    }

    //data finished loading
    if (self.mode == self.mode_enum.loading){
      if(!data.loading){
        self.mode = self.mode_enum[data.state]
        self.timerBase = data.deltaTime
      }
    }
    
    if (data.run_ended){
      self.timerBase = self.timerBase + Date.now() - self.timerStarted
      self.timerStarted = null
      self.mode = self.mode_enum.end
    }

    if (data.loading_msg)
      self.loading_msg = data.loading_msg

    
    if (self.mode == self.mode_enum.start || self.mode == self.mode_enum.start){
      self.refreshRunData = false
    }
    else self.refreshRunData = true
    
    setTimeout(()=>{
        if (self.refreshRunData) updateRunInfo(self)
    }, 250)
  })
}

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
