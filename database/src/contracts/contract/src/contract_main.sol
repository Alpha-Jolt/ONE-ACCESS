pragma solidity ^0.8.0;

// Import the required Oracle interface
import "./OracleInterface.sol";

contract DatabaseConnector {
    // Declare the Oracle contract instance
    OracleInterface private oracle;
    
    // Event to emit when new data is fetched from the database
    event DataFetched(uint256 id, string data);
    
    // Initialize the Oracle contract address
    constructor(address oracleAddress) {
        oracle = OracleInterface(oracleAddress);
    }
    
    // Function to fetch data from the database
    function fetchData(uint256 id) external {
        // Call the Oracle contract's getData function to retrieve data from the database
        string memory data = oracle.getData(id);
        
        // Emit an event with the fetched data
        emit DataFetched(id, data);
    }
}
