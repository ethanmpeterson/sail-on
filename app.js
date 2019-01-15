const express = require('express')
var cors = require('cors')
const app = express()
let {PythonShell} = require('python-shell')

app.use(cors())

var port = process.env.PORT || 3000;

const testData = {
	"testData": [
		{
			"lat" : 0,
			"lon" : 0
		},
		{
			"lat" : 25,
			"lon" : 25
		}
	]
};

// app.get('/', function (req, res) {
// 	res.send(testData)
// })

app.get('/', callScript);
	// const spawn = require("child_process").spawn
	// const pythonProcess = spawn('python',["path_finding.py", '1', '2', '3', '4']);
	// pythonProcess.stdout.on('data', (data) => {
	// 	res.send(data.toString())
	// });
	// //console.log("YEET")
	// //res.send(testData)


function callScript(req, res) {
	var options = {
		args:
		[
			req.lat1,
			req.lon1,
			req.lat2,
			req.lon2
		]
	  }
	
	  PythonShell.run('path_finding.py', options, function (err, data) {
		if (err) res.send(err);
		res.send(JSON.parse(data))
	  });
}

app.listen(port, () => console.log(`listening on port ${port}!`))

