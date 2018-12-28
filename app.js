const express = require('express')
var cors = require('cors')
const app = express()

app.use(cors())

const port = 80

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

app.get('/', (req, res) => res.send(testData))

app.listen(port, () => console.log(`listening on port ${port}!`))

