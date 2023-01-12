const express = require('express')

const bodyParser = require('body-parser')
const { v4: uuid } = require('uuid')
const axios = require('axios')
const fs = require('fs')

const app = express()
const port = 3000


app.use(bodyParser.urlencoded({ extended: true }))
app.use(bodyParser.json({ limit: '60MB' }))

app.use(express.static('public'))

const Test = () => {
    axios.post("http://127.0.0.1:5000/process/image", { fileName: '03.jpg' })
    .then(res => {
        console.log(res.data)
    }).catch(e => {
        console.log(e)
    })
}

app.post('/analyze', (req, res) => {
    const data = req.body
    const uniqueFileName = `test.jpg`

    fs.writeFile(`./public/${uniqueFileName}`, data.image, 'base64', (err) => {
        if(err) {
            res.json({ error: 'File Save Error!' })
            console.log(err)
            return
        }
    })

    const requestData = {
        fileName: uniqueFileName
    }

    axios.post("http://127.0.0.1:5000/process/image", requestData)
    .then(response => {
        console.log(response.data)
        res.json(response.data)
        return
    }).catch(err => {
        console.log(err)
        res.json({ error: 'Analysis API Error!' })
    })
})

app.listen(port, () => {
    console.log(`Server is Listening on ${port}`)
})