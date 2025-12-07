CREATE CONSTRAINT IF NOT EXISTS FOR (n:BMWModel) REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Series) REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (n:BodyType) REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Powertrain) REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Drivetrain) REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Feature) REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Performance) REQUIRE n.name IS UNIQUE;
MERGE (:Series {name: '1 Series'});
MERGE (:Series {name: '2 Series'});
MERGE (:Series {name: '3 Series'});
MERGE (:Series {name: '4 Series'});
MERGE (:Series {name: '5 Series'});
MERGE (:Series {name: '6 Series'});
MERGE (:Series {name: '7 Series'});
MERGE (:Series {name: '8 Series'});
MERGE (:Series {name: 'X Series'});
MERGE (:Series {name: 'i Series'});
MERGE (:Series {name: 'M Series'});
MERGE (:Series {name: 'Z Series'});
MERGE (:BodyType {name: 'Sedan'});
MERGE (:BodyType {name: 'SUV'});
MERGE (:BodyType {name: 'Coupe'});
MERGE (:BodyType {name: 'Gran Coupe'});
MERGE (:BodyType {name: 'Convertible'});
MERGE (:BodyType {name: 'Hatchback'});
MERGE (:Powertrain {name: 'Gasoline'});
MERGE (:Powertrain {name: 'Diesel'});
MERGE (:Powertrain {name: 'Hybrid'});
MERGE (:Powertrain {name: 'Plug-in Hybrid'});
MERGE (:Powertrain {name: 'Electric'});
MERGE (:Drivetrain {name: 'FWD'});
MERGE (:Drivetrain {name: 'RWD'});
MERGE (:Drivetrain {name: 'AWD'});
MERGE (:Feature {name: 'xDrive'});
MERGE (:Feature {name: 'iDrive'});
MERGE (:Feature {name: 'Driving Assistance'});
MERGE (:Feature {name: 'Driving Assistance Pro'});
MERGE (:Feature {name: 'M Sport Suspension'});
MERGE (:Feature {name: 'Panoramic Roof'});
MERGE (:Performance {name: 'Standard'});
MERGE (:Performance {name: 'M Performance'});
MERGE (:Performance {name: 'M Series'});
MERGE (m:BMWModel:ElectricCar:HighPerformanceCar:AdvancedADASCar:iSeriesCar:AWDCar {name: 'BMW i4 M50'})
WITH m MATCH (s:Series {name: 'i Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Gran Coupe'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Electric'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'AWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'M Performance'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'xDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'Driving Assistance Pro'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:HighPerformanceCar:ThreeSeriesCar:RWDCar {name: 'BMW M3 G80'})
WITH m MATCH (s:Series {name: '3 Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Sedan'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'RWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'M Series'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'M Sport Suspension'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:HybridCar:StandardCar:OffroadCapableSUV:XSeriesCar:AWDCar {name: 'BMW X5 xDrive45e'})
WITH m MATCH (s:Series {name: 'X Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'SUV'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Plug-in Hybrid'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'AWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'xDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'Driving Assistance'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'Panoramic Roof'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:StandardCar:ThreeSeriesCar:RWDCar {name: 'BMW 320i F30'})
WITH m MATCH (s:Series {name: '3 Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Sedan'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'RWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:ElectricCar:StandardCar:AdvancedADASCar:OffroadCapableSUV:iSeriesCar:AWDCar {name: 'BMW iX xDrive50'})
WITH m MATCH (s:Series {name: 'i Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'SUV'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Electric'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'AWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'xDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'Driving Assistance Pro'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:HybridCar:StandardCar:AWDCar {name: 'BMW 530e G30'})
WITH m MATCH (s:Series {name: '5 Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Sedan'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Plug-in Hybrid'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'AWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'Driving Assistance'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:HighPerformanceCar:AdvancedADASCar:AWDCar {name: 'BMW M5 F90'})
WITH m MATCH (s:Series {name: '5 Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Sedan'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'AWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'M Series'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'xDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'M Sport Suspension'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'Driving Assistance Pro'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:StandardCar:OffroadCapableSUV:XSeriesCar:AWDCar {name: 'BMW X3 xDrive30i'})
WITH m MATCH (s:Series {name: 'X Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'SUV'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'AWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'xDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'Panoramic Roof'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'Driving Assistance'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:StandardCar:OffroadCapableSUV:XSeriesCar:AWDCar {name: 'BMW X1 xDrive20i'})
WITH m MATCH (s:Series {name: 'X Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'SUV'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'AWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'xDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:StandardCar:RWDCar {name: 'BMW 420i Gran Coupe'})
WITH m MATCH (s:Series {name: '4 Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Gran Coupe'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'RWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'Driving Assistance'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:StandardCar:OffroadCapableSUV:XSeriesCar:AWDCar {name: 'BMW X2 xDrive20i'})
WITH m MATCH (s:Series {name: 'X Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'SUV'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'AWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'xDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:StandardCar:OffroadCapableSUV:XSeriesCar:AWDCar {name: 'BMW X4 xDrive30i'})
WITH m MATCH (s:Series {name: 'X Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'SUV'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'AWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'xDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'Panoramic Roof'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:HighPerformanceCar:OffroadCapableSUV:XSeriesCar:AWDCar {name: 'BMW X6 M50i'})
WITH m MATCH (s:Series {name: 'X Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'SUV'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'AWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'M Performance'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'xDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'M Sport Suspension'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:HighPerformanceCar:AdvancedADASCar:RWDCar {name: 'BMW 8 Series Gran Coupe'})
WITH m MATCH (s:Series {name: '8 Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Gran Coupe'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'RWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'M Series'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'Driving Assistance Pro'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:HighPerformanceCar:AdvancedADASCar:CoupeCar:RWDCar {name: 'BMW M4 Competition'})
WITH m MATCH (s:Series {name: '4 Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Coupe'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'RWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'M Series'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'M Sport Suspension'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'Driving Assistance Pro'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:HighPerformanceCar:ConvertibleCar:RWDCar {name: 'BMW Z4 M40i'})
WITH m MATCH (s:Series {name: 'Z Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Convertible'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'RWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'M Performance'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'M Sport Suspension'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:ElectricCar:StandardCar:iSeriesCar:HatchbackCar:RWDCar {name: 'BMW i3 (2024)'})
WITH m MATCH (s:Series {name: 'i Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Hatchback'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Electric'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'RWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:ElectricCar:StandardCar:AdvancedADASCar:iSeriesCar:AWDCar {name: 'BMW i7 xDrive60'})
WITH m MATCH (s:Series {name: 'i Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Sedan'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Electric'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'AWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'Driving Assistance Pro'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:HybridCar:HighPerformanceCar:OffroadCapableSUV:XSeriesCar:AWDCar {name: 'BMW XM M Hybrid'})
WITH m MATCH (s:Series {name: 'X Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'SUV'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Plug-in Hybrid'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'AWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'M Series'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'xDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'M Sport Suspension'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:HighPerformanceCar:AdvancedADASCar:AWDCar {name: 'BMW 7 Series 760i'})
WITH m MATCH (s:Series {name: '7 Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Sedan'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'AWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'M Performance'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'Driving Assistance Pro'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:StandardCar:RWDCar {name: 'BMW 6 Series Gran Turismo'})
WITH m MATCH (s:Series {name: '6 Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Gran Coupe'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'RWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'Panoramic Roof'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'Driving Assistance'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:StandardCar:RWDCar {name: 'BMW 2 Series Gran Coupe'})
WITH m MATCH (s:Series {name: '2 Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Gran Coupe'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'RWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:HighPerformanceCar:CoupeCar:RWDCar {name: 'BMW M2 Competition'})
WITH m MATCH (s:Series {name: '2 Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Coupe'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'RWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'M Series'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'M Sport Suspension'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:ElectricCar:StandardCar:iSeriesCar:RWDCar {name: 'BMW i5 eDrive40'})
WITH m MATCH (s:Series {name: 'i Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Sedan'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Electric'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'RWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'Driving Assistance'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:HighPerformanceCar:HatchbackCar:AWDCar {name: 'BMW 1 Series M135i'})
WITH m MATCH (s:Series {name: '1 Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Hatchback'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'AWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'M Performance'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'xDrive'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:StandardCar:RWDCar {name: 'BMW 6 Series GT 630i'})
WITH m MATCH (s:Series {name: '6 Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Gran Coupe'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'RWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'Panoramic Roof'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:HighPerformanceCar:AdvancedADASCar:CoupeCar:RWDCar {name: 'BMW M8 Competition'})
WITH m MATCH (s:Series {name: '8 Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Coupe'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'RWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'M Series'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'M Sport Suspension'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'Driving Assistance Pro'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:StandardCar:OffroadCapableSUV:XSeriesCar:AWDCar {name: 'BMW X7 xDrive40i'})
WITH m MATCH (s:Series {name: 'X Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'SUV'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'AWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'xDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'Panoramic Roof'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:StandardCar:ConvertibleCar:RWDCar {name: 'BMW Z4 sDrive20i'})
WITH m MATCH (s:Series {name: 'Z Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Convertible'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'RWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:HighPerformanceCar:OffroadCapableSUV:XSeriesCar:AWDCar {name: 'BMW X3 M40i'})
WITH m MATCH (s:Series {name: 'X Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'SUV'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'AWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'M Performance'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'xDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'M Sport Suspension'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:HighPerformanceCar:OffroadCapableSUV:XSeriesCar:AWDCar {name: 'BMW X4 M40i'})
WITH m MATCH (s:Series {name: 'X Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'SUV'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'AWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'M Performance'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'xDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'M Sport Suspension'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:ElectricCar:StandardCar:OffroadCapableSUV:iSeriesCar:RWDCar {name: 'BMW iX3'})
WITH m MATCH (s:Series {name: 'i Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'SUV'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Electric'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'RWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'xDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:HighPerformanceCar:RWDCar {name: 'BMW 5 Series M550i'})
WITH m MATCH (s:Series {name: '5 Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Sedan'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'RWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'M Performance'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'M Sport Suspension'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:DieselCar:StandardCar:OffroadCapableSUV:XSeriesCar:AWDCar {name: 'BMW X6 xDrive30d'})
WITH m MATCH (s:Series {name: 'X Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'SUV'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Diesel'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'AWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'xDrive'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:StandardCar:HatchbackCar:FWDCar {name: 'BMW 118i'})
WITH m MATCH (s:Series {name: '1 Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Hatchback'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'FWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:StandardCar:CoupeCar:RWDCar {name: 'BMW 230i Coupe'})
WITH m MATCH (s:Series {name: '2 Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Coupe'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'RWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:HybridCar:StandardCar:ThreeSeriesCar:RWDCar {name: 'BMW 330e'})
WITH m MATCH (s:Series {name: '3 Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Sedan'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Plug-in Hybrid'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'RWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'Driving Assistance'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:StandardCar:RWDCar {name: 'BMW 540i'})
WITH m MATCH (s:Series {name: '5 Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Sedan'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'RWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:StandardCar:RWDCar {name: 'BMW 750Li'})
WITH m MATCH (s:Series {name: '7 Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Sedan'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'RWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'Standard'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'Driving Assistance'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:HighPerformanceCar:OffroadCapableSUV:XSeriesCar:AWDCar {name: 'BMW X5 M Competition'})
WITH m MATCH (s:Series {name: 'X Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'SUV'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'AWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'M Series'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'xDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'M Sport Suspension'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:HighPerformanceCar:AWDCar {name: 'BMW M440i Gran Coupe'})
WITH m MATCH (s:Series {name: '4 Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Gran Coupe'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'AWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'M Performance'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'xDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'M Sport Suspension'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:HighPerformanceCar:OffroadCapableSUV:XSeriesCar:AWDCar {name: 'BMW X2 M35i'})
WITH m MATCH (s:Series {name: 'X Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'SUV'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'AWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'M Performance'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'xDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'M Sport Suspension'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:ElectricCar:HighPerformanceCar:AdvancedADASCar:iSeriesCar:AWDCar {name: 'BMW i7 M70'})
WITH m MATCH (s:Series {name: 'i Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Sedan'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Electric'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'AWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'M Series'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'iDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'Driving Assistance Pro'}) MERGE (m)-[:HAS_FEATURE]->(f);
MERGE (m:BMWModel:PetrolCar:HighPerformanceCar:CoupeCar:AWDCar {name: 'BMW M850i xDrive'})
WITH m MATCH (s:Series {name: '8 Series'}) MERGE (m)-[:HAS_SERIES]->(s)
WITH m MATCH (b:BodyType {name: 'Coupe'}) MERGE (m)-[:HAS_BODY_TYPE]->(b)
WITH m MATCH (p:Powertrain {name: 'Gasoline'}) MERGE (m)-[:HAS_POWERTRAIN]->(p)
WITH m MATCH (d:Drivetrain {name: 'AWD'}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)
WITH m MATCH (perf:Performance {name: 'M Performance'}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)
WITH m MATCH (f:Feature {name: 'xDrive'}) MERGE (m)-[:HAS_FEATURE]->(f)
WITH m MATCH (f:Feature {name: 'M Sport Suspension'}) MERGE (m)-[:HAS_FEATURE]->(f);