"""Cypher query generator from JSON data."""

import json
import logging
import os
import re

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Node labels for powertrains
POWERTRAIN_LABELS = {
    "Electric": "ElectricCar",
    "Plug-in Hybrid": "HybridCar",
    "Gasoline": "PetrolCar",
    "Diesel": "DieselCar",
}

# Node labels for performance types
PERFORMANCE_LABELS = {
    "M Series": "HighPerformanceCar",
    "M Performance": "HighPerformanceCar",
    "Standard": "StandardCar",
}

# Node labels for series types
SERIES_LABELS = {
    "i Series": "iSeriesCar",
    "3 Series": "ThreeSeriesCar",
    "X Series": "XSeriesCar",
}

# Node labels for body types
BODY_TYPE_LABELS = {
    "Coupe": "CoupeCar",
    "Convertible": "ConvertibleCar",
    "Hatchback": "HatchbackCar",
}

# Node labels for drivetrain types
DRIVETRAIN_LABELS = {
    "FWD": "FWDCar",
    "RWD": "RWDCar",
    "AWD": "AWDCar",
}


def clean_string(s: str) -> str:
    """Clean and escape a string for Cypher queries."""
    return s.strip().replace("'", "\\'")


def to_snake_case(name: str) -> str:
    """Convert a string to snake_case."""
    s = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    return s.replace(" ", "_").replace("-", "_")


def _create_constraints() -> list[str]:
    """Generate constraint creation queries."""
    node_types = [
        "BMWModel",
        "Series",
        "BodyType",
        "Powertrain",
        "Drivetrain",
        "Feature",
        "Performance",
    ]
    return [
        f"CREATE CONSTRAINT IF NOT EXISTS FOR (n:{node_type}) REQUIRE n.name IS UNIQUE;"
        for node_type in node_types
    ]


def _create_reference_nodes(data: dict) -> list[str]:
    """Generate MERGE queries for reference nodes."""
    queries = []
    node_mappings = {
        "series": "Series",
        "body_types": "BodyType",
        "powertrains": "Powertrain",
        "drivetrains": "Drivetrain",
        "features": "Feature",
        "performances": "Performance",
    }

    for data_key, node_label in node_mappings.items():
        for item in data.get(data_key, []):
            queries.append(f"MERGE (:{node_label} {{name: '{clean_string(item)}'}});")

    return queries


def _get_model_labels(model: dict) -> list[str]:
    labels = ["BMWModel"]
    powertrain = model["powertrain"]
    performance = model["performance"]
    body_type = model["body_type"]
    drivetrain = model["drivetrain"]
    series = model["series"]
    features = model["features"]

    # Powertrain-based labels
    if powertrain in POWERTRAIN_LABELS:
        labels.append(POWERTRAIN_LABELS[powertrain])

    # Performance-based labels
    if performance in PERFORMANCE_LABELS:
        labels.append(PERFORMANCE_LABELS[performance])

    # Feature-based labels
    if "Driving Assistance Pro" in features:
        labels.append("AdvancedADASCar")

    # SUV with xDrive capability
    if body_type == "SUV" and "xDrive" in features:
        labels.append("OffroadCapableSUV")

    # Series-based labels
    if series in SERIES_LABELS:
        labels.append(SERIES_LABELS[series])

    # Body type-based labels
    if body_type in BODY_TYPE_LABELS:
        labels.append(BODY_TYPE_LABELS[body_type])

    # Drivetrain-based labels
    if drivetrain in DRIVETRAIN_LABELS:
        labels.append(DRIVETRAIN_LABELS[drivetrain])

    return labels


def _create_model_query(model: dict) -> str:
    name = clean_string(model["name"])
    series = clean_string(model["series"])
    body_type = clean_string(model["body_type"])
    powertrain = clean_string(model["powertrain"])
    drivetrain = clean_string(model["drivetrain"])
    performance = clean_string(model["performance"])
    features = [clean_string(f) for f in model["features"]]

    labels = _get_model_labels(model)
    label_str = ":" + ":".join(labels)

    # Build query parts
    query_parts = [
        f"MERGE (m{label_str} {{name: '{name}'}})",
        f"WITH m MATCH (s:Series {{name: '{series}'}}) MERGE (m)-[:HAS_SERIES]->(s)",
        f"WITH m MATCH (b:BodyType {{name: '{body_type}'}}) MERGE (m)-[:HAS_BODY_TYPE]->(b)",
        f"WITH m MATCH (p:Powertrain {{name: '{powertrain}'}}) MERGE (m)-[:HAS_POWERTRAIN]->(p)",
        f"WITH m MATCH (d:Drivetrain {{name: '{drivetrain}'}}) MERGE (m)-[:HAS_DRIVETRAIN]->(d)",
        f"WITH m MATCH (perf:Performance {{name: '{performance}'}}) MERGE (m)-[:HAS_PERFORMANCE]->(perf)",
    ]

    # Add feature relationships
    for feature in features:
        query_parts.append(
            f"WITH m MATCH (f:Feature {{name: '{feature}'}}) MERGE (m)-[:HAS_FEATURE]->(f)"
        )

    return "\n".join(query_parts) + ";"


def generate_cypher(data_file: str, output_file: str) -> None:
    if not os.path.exists(data_file):
        logger.error(f"{data_file} not found.")
        return

    with open(data_file, "r") as f:
        data = json.load(f)

    cypher_queries = []

    # Add constraints
    cypher_queries.extend(_create_constraints())

    # Add reference nodes
    cypher_queries.extend(_create_reference_nodes(data))

    # Add model nodes and relationships
    for model in data.get("models", []):
        cypher_queries.append(_create_model_query(model))

    # Write to output file
    with open(output_file, "w") as f:
        f.write("\n".join(cypher_queries))

    logger.info(f"Generated {len(cypher_queries)} Cypher queries in {output_file}")


if __name__ == "__main__":
    generate_cypher("data/data.json", "data/graph_data.cypher")
