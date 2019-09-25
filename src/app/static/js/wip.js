var app = new Vue({
  el: '#app',
  delimiters: ['${', '}'],
  data: {
  	battery_percentage: 88,
  	robot_name: "turty3_pro",
  	mode_enum: {
  		start: 0,
   		run: 1,
    	pause: 2,
  	},
    mode: 0,
    past_runs: [
    	{
    		name: "run_1",
    		path: "/path/to/run_1/",
    		date: "2019-09-25",
    		length: "8:22",
    	},
    	{
    		name: "run_2",
    		path: "/path/to/run_2/",
    		date: "2019-09-25",
    		length: "8:22",
    	},
    	{
    		name: "run_3",
    		path: "/path/to/run_3/",
    		date: "2019-09-25",
    		length: "8:22",
    	},
    	{
    		name: "run_4",
    		path: "/path/to/run_4/",
    		date: "2019-09-25",
    		length: "8:22",
    	},
    	{
    		name: "run_5",
    		path: "/path/to/run_4/",
    		date: "2019-09-25",
    		length: "8:22",
    	},
    ],
  },
  computed: {
  	battery: function(){
  		//returns the correct icon based on battery percentage
  		if (this.battery_percentage > 90) return "fas fa-battery-full"
  		if (this.battery_percentage > 65) return "fas fa-battery-three-quarters"
  		if (this.battery_percentage > 32) return "fas fa-battery-half"
  		if (this.battery_percentage > 10) return "fas fa-battery-quarter"
  		return "fas fa-battery-empty"
  	}
  }
})