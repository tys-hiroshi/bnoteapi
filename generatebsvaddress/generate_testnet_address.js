const bsv = require('bsv')
const privateKey = bsv.PrivateKey.fromRandom('testnet')
console.log(privateKey.toWIF())
const address = bsv.Address.fromPrivateKey(privateKey, 'testnet')
console.log(address.toString())

// cToTwJbnmX91vKSaDWBkmmrP25MVKzQPFCCiGQu773xFybSj1dLg
// munS9K3pwpYRVoDto4hNCTEKjoUQQQykdh