SET search_path TO naval_world, public ;

DROP SCHEMA IF EXISTS NAVAL_WORLD CASCADE;

CREATE SCHEMA NAVAL_WORLD;
SET search_path TO NAVAL_WORLD, public;

CREATE TABLE Country (
  country_id INT PRIMARY KEY,
  country_name VARCHAR(42),
  country_money INT,
  country_power INT,
  surface INT
);

CREATE TABLE Country_Affection (
  country_id_in INT REFERENCES Country(country_id),
  country_id_out INT REFERENCES Country(country_id),
  score FLOAT,

  PRIMARY KEY(country_id_in, country_id_out)
);

CREATE TABLE Region (
  region_id INT PRIMARY KEY,
  region_name VARCHAR(200),
  latitude FLOAT,
  longitude FLOAT
);

CREATE TABLE Country_Region (
  country_id INT REFERENCES Country(country_id),
  region_id INT REFERENCES Region(region_id),

  PRIMARY KEY(country_id, region_id)
);

CREATE TABLE Batiment_type (
  batiment_type_id INT PRIMARY KEY,
  batiment_type_name VARCHAR(50),
  batiment_power INT,
  max_health INT,
  costOfProductionInMillions INT
);

CREATE TABLE Batiment (
  batiment_id INT PRIMARY KEY,
  region_id INT REFERENCES Region(region_id),
  batiment_type_id INT REFERENCES Batiment_type(batiment_type_id),
  batiment_name VARCHAR(30),
  latitude FLOAT,
  longitude FLOAT,
  health INT,
  comment VARCHAR(2048),
  state INT -- 0: actif 1: en vente (inactif)
);

CREATE TABLE Action_Batiment (
  action_id SERIAL PRIMARY KEY,
  batiment_id INT REFERENCES Batiment(batiment_id),
  goalLat FLOAT,
  goalLong FLOAT
);


CREATE TABLE Contract (
  contract_id SERIAL PRIMARY KEY,
  region_id_seller INT REFERENCES Region(region_id),
  batiment_id INT REFERENCES Batiment(batiment_id),
  minCost INT,
  maxCost INT,
  tau INT,
  r INT,
  date_creating DATE,
  active INT
);

CREATE TABLE Command (
  command_id SERIAL PRIMARY KEY,
  contract_id SERIAL REFERENCES Contract(contract_id),
  region_id_buyer INT REFERENCES Region(region_id),
  date_buy DATE,
  price INT
);

-- TRIGGER


CREATE OR REPLACE FUNCTION SetDefaultCountryAffection()
RETURNS TRIGGER
AS $$
  DECLARE
    country Country%rowtype;
  BEGIN
    FOR country IN (
        SELECT *
        FROM Country
      ) LOOP
      INSERT INTO Country_Affection(country_id_in, country_id_out, score)
      VALUES (new.country_id, country.country_id, 40)
      ON CONFLICT (country_id_in, country_id_out)
      DO NOTHING;

      INSERT INTO Country_Affection(country_id_in, country_id_out, score)
      VALUES (country.country_id, new.country_id, 60)
      ON CONFLICT (country_id_in, country_id_out)
      DO NOTHING;

      END LOOP;
    RETURN new;
  END;
$$ LANGUAGE PLPGSQL;

CREATE TRIGGER SetDefaultCountryAffection
AFTER INSERT ON Country
FOR EACH ROW
EXECUTE PROCEDURE SetDefaultCountryAffection();
