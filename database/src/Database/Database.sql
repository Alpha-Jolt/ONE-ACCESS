-- Create the user_profile table
CREATE TABLE user_profile (
  id SERIAL PRIMARY KEY,
  User_name VARCHAR(100) NOT NULL,
  Time_Stamp TIMESTAMP DEFAULT NOW()
);

-- Create the biometric_details table
CREATE TABLE biometric_details (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES user_profile(id),
  fingerprint_data BYTEA NOT NULL,
  Time_stamp TIMESTAMP DEFAULT NOW()
);

-- Function to insert a new user profile
CREATE OR REPLACE FUNCTION insert_user_profile(
  p_User_name VARCHAR(100),
) RETURNS INTEGER AS $$
DECLARE
  user_id INTEGER;
BEGIN
  INSERT INTO user_profile (User_name)
  VALUES (p_User_name)
  RETURNING id INTO user_id;
  
  RETURN user_id;
END;
$$ LANGUAGE plpgsql;

-- Function to insert biometric details for a user
CREATE OR REPLACE FUNCTION insert_biometric_details(
  p_user_id INTEGER,
  p_fingerprint_data BYTEA
) RETURNS VOID AS $$
BEGIN
  INSERT INTO biometric_details (user_id, fingerprint_data)
  VALUES (p_user_id, p_fingerprint_data);
END;
$$ LANGUAGE plpgsql;

-- Trigger function to insert biometric details after a user profile is inserted
CREATE OR REPLACE FUNCTION insert_biometric_after_user_profile()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO biometric_details (user_id, fingerprint_data)
  VALUES (NEW.id, NEW.fingerprint_data);
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger to insert biometric details after user profile insertion
CREATE TRIGGER insert_biometric
AFTER INSERT ON user_profile
FOR EACH ROW
EXECUTE FUNCTION insert_biometric_after_user_profile();