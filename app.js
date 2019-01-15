const express = require('express')
var cors = require('cors')
const app = express()

app.use(cors())

const port = 3000

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

app.get('/', function (req, res) {
	res.send(testData)
})

app.post('/', function (req, res) {
	const spawn = require("child_process").spawn
	const pythonProcess = spawn('python',["path_finding.py", '1', '2', '3', '4']);
})

app.listen(port, () => console.log(`listening on port ${port}!`))

