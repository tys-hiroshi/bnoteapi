const bsv = require('bsv')
const privateKey = bsv.PrivateKey.fromRandom()
console.log(privateKey.toWIF())
const address = bsv.Address.fromPrivateKey(privateKey)
console.log(address.toString())

