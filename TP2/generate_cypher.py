import json
import re
import os


def clean_string(s):
    return s.strip().replace("'", "\\'")


def to_snake_case(name):
    s = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    return s.replace(" ", "_").replace("-", "_")


def generate_cypher(data_file, output_file):
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found.")
        return

    with open(data_file, "r") as f:
        data = json.load(f)

    cypher_queries = []

    # Create Constraints
    cypher_queries.append(
        "CREATE CONSTRAINT IF NOT EXISTS FOR (n:BMWModel) REQUIRE n.name IS UNIQUE;"
    )
    cypher_queries.append(
        "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Series) REQUIRE n.name IS UNIQUE;"
    )
    cypher_queries.append(
        "CREATE CONSTRAINT IF NOT EXISTS FOR (n:BodyType) REQUIRE n.name IS UNIQUE;"
    )
    cypher_queries.append(
        "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Powertrain) REQUIRE n.name IS UNIQUE;"
    )
    cypher_queries.append(
        "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Drivetrain) REQUIRE n.name IS UNIQUE;"
    )
    cypher_queries.append(
        "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Feature) REQUIRE n.name IS UNIQUE;"
    )
    cypher_queries.append(
        "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Performance) REQUIRE n.name IS UNIQUE;"
    )

    # Create Reference Nodes
    for item in data.get("series", []):
        cypher_queries.append(f"MERGE (:Series {{name: '{clean_string(item)}'}});")

    for item in data.get("body_types", []):
        cypher_queries.append(f"MERGE (:BodyType {{name: '{clean_string(item)}'}});")

    for item in data.get("powertrains", []):
        cypher_queries.append(f"MERGE (:Powertrain {{name: '{clean_string(item)}'}});")

    for item in data.get("drivetrains", []):
        cypher_queries.append(f"MERGE (:Drivetrain {{name: '{clean_string(item)}'}});")

    for item in data.get("features", []):
        cypher_queries.append(f"MERGE (:Feature {{name: '{clean_string(item)}'}});")

    for item in data.get("performances", []):
        cypher_queries.append(f"MERGE (:Performance {{name: '{clean_string(item)}'}});")

    # Create Models and Relationships
    for model in data.get("models", []):
        name = clean_string(model["name"])
        series = clean_string(model["series"])
        body_type = clean_string(model["body_type"])
        powertrain = clean_string(model["powertrain"])
        drivetrain = clean_string(model["drivetrain"])
        performance = clean_string(model["performance"])
        features = [clean_string(f) for f in model["features"]]

        # Base Label
        labels = ["BMWModel"]

        # Prolog Logic Translation
        if powertrain == "Electric":
            labels.append("ElectricCar")

        if powertrain == "Plug-in Hybrid":
            labels.append("HybridCar")

        if powertrain == "Gasoline":
            labels.append("PetrolCar")

        if powertrain == "Diesel":
            labels.append("DieselCar")

        if performance in ["M Series", "M Performance"]:
            labels.append("HighPerformanceCar")

        if performance == "Standard":
            labels.append("StandardCar")

        if "Driving Assistance Pro" in features:
            labels.append("AdvancedADASCar")

        if body_type == "SUV" and "xDrive" in features:
            labels.append("OffroadCapableSUV")

        if series == "i Series":
            labels.append("iSeriesCar")

        if series == "3 Series":
            labels.append("ThreeSeriesCar")

        if series == "X Series":
            labels.append("XSeriesCar")

        if body_type == "Coupe":
            labels.append("CoupeCar")

        if body_type == "Convertible":
            labels.append("ConvertibleCar")

        if body_type == "Hatchback":
            labels.append("HatchbackCar")

        if drivetrain == "FWD":
            labels.append("FWDCar")

        if drivetrain == "RWD":
            labels.append("RWDCar")

        if drivetrain == "AWD":
            labels.append("AWDCar")

        label_str = ":" + ":".join(labels)

        # Create Model Node and all relationships in a single chained query
        query_parts = [f"MERGE (m{label_str} {{name: '{name}'}})"]
        query_parts.append(
            f"WITH m MATCH (s:Series {{name: '{series}'}}) MERGE (m)-[:HAS_SERIES]->(s)"
        )
        query_parts.append(
            f"WITH m MATCH (b:BodyType {{name: '{body_type}'}}) MERGE (m)-[:HAS_BODY_TYPE]->(b)"
        )
        query_parts.append(
            f"WITH m MATCH (p:Powertrain {{name: '{powertrain}'}}) MERGE (m)-[:HAS_POWERTRAIN]->(p)"
        )
        query_parts.append(
            f"WITH m MATCH (d:Drivetrain {{name: '{drivetrain}'}}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)"
        )
        query_parts.append(
            f"WITH m MATCH (perf:Performance {{name: '{performance}'}}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)"
        )

        for feature in features:
            query_parts.append(
                f"WITH m MATCH (f:Feature {{name: '{feature}'}}) MERGE (m)-[:HAS_FEATURE]->(f)"
            )

        cypher_queries.append("\n".join(query_parts) + ";")

    with open(output_file, "w") as f:
        f.write("\n".join(cypher_queries))

    print(f"Generated {len(cypher_queries)} Cypher queries in {output_file}")


if __name__ == "__main__":
    generate_cypher("../TP1/data.json", "graph_data.cypher")
