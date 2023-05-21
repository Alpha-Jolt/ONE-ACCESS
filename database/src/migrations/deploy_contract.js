const MyContract = artifacts.require("main");

module.exports = function(deployer) {
  deployer.deploy(MyContract);
};