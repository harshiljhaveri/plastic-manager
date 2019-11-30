
Account = null
App = {}

   async function init()  {
    if (App.web3Provider != null) {
      return;
    }
    if (window.ethereum) {
      App.web3Provider = window.ethereum;
      try {
        await window.ethereum.enable();
      } catch (error) {
        console.error("User denied account access");
      }
    } else if (window.web3) {
      App.web3Provider = window.web3.currentProvider;
    }
    // If no injected web3 instance is detected, fall back to Ganache
    else {
      App.web3Provider = new Web3.providers.HttpProvider(
        "http://localhost:8545"
      );
    }
    App.web3 = new Web3(App.web3Provider);
    getAddress()
  }

  


function login(email,password) {
    return firebase.auth().signInWithEmailAndPassword(email, password);
}

function signup(name,email,password,address) {
    firebase.auth().createUserWithEmailAndPassword(email, password).then(() => login(email,password))
        .then(() => {
            var user = firebase.auth().currentUser;
            console.log(name + "@" + address)
            return new Promise((res,rek) => {
                user.updateProfile({
                    displayName: name + "@" + address
                })
                var database = firebase.database();
                database.ref('users').child(email.replace("@","AT").replace(".",",")).set({
                    address : address
                });
                res()
            })
        });     
}


function getAddress() {
    let i = 1;
    return new Promise((res, rej) => {
        web3.eth.getCoinbase(function(err, account) {
          if (err === null) {
            Account = account;
            $("#address").html("Your Account: " + account);
          }
          i++;
          if (i == 2) {
            res();
          }
        });
      });
}

