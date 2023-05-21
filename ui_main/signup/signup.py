const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');

const app = express();

// parse incoming request data
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// connect to MongoDB database
mongoose.connect('mongodb://localhost/mydatabase', { useNewUrlParser: true });

// define a user schema and model
const userSchema = new mongoose.Schema({
  username: { type: String, required: true, unique: true }
});
const User = mongoose.model('User', userSchema);

// handle form submission
app.post('/submit', async (req, res) => {
  const { username } = req.body;

  try {
    // create a new user document in the database
    const user = new User({ username });
    await user.save();
    
    res.send('Username successfully created!');
  } catch (err) {
    // handle errors such as duplicate username
    res.status(400).send(err.message);
  }
});

// start the server
app.listen(3000, () => {
  console.log('Server listening on port 3000');
});