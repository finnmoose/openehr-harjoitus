import argparse
import json
import sys


REQUIRED_FIELDS = ["time", "systolic_mmHg", "diastolic_mmHg", "mean_arterial_pressure_mmHg", "pulse_per_min"]


def load_observation(filename):
    """Load and validate blood pressure observation from an OpenEHR JSON file."""
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "observation" not in data:
        raise KeyError("observation")

    obs = data["observation"]

    missing = [field for field in REQUIRED_FIELDS if field not in obs]
    if missing:
        raise KeyError(", ".join(missing))

    return obs


def print_blood_pressure(obs):
    """Print blood pressure data in human-readable format."""
    print("Blood pressure")
    print("Time:", obs["time"])
    print("Sys:", obs["systolic_mmHg"], "mmHg")
    print("Dia:", obs["diastolic_mmHg"], "mmHg")
    print("MAP:", obs["mean_arterial_pressure_mmHg"], "mmHg")
    print("Pulse:", obs["pulse_per_min"], "bpm")

    # Single-line summary for logs
    print(f"BP: {obs['systolic_mmHg']}/{obs['diastolic_mmHg']} mmHg, MAP: {obs['mean_arterial_pressure_mmHg']} mmHg, Pulse: {obs['pulse_per_min']} bpm @ {obs['time']}")


def to_fhir_observation(obs):
    """Convert OpenEHR blood pressure observation to FHIR R4 Observation."""
    return {
        "resourceType": "Observation",
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                        "code": "vital-signs",
                        "display": "Vital Signs"
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "85354-9",
                    "display": "Blood pressure panel with all children optional"
                }
            ],
            "text": "Blood pressure"
        },
        "effectiveDateTime": obs["time"],
        "component": [
            {
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "8480-6",
                            "display": "Systolic blood pressure"
                        }
                    ]
                },
                "valueQuantity": {
                    "value": obs["systolic_mmHg"],
                    "unit": "mmHg",
                    "system": "http://unitsofmeasure.org",
                    "code": "mm[Hg]"
                }
            },
            {
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "8462-4",
                            "display": "Diastolic blood pressure"
                        }
                    ]
                },
                "valueQuantity": {
                    "value": obs["diastolic_mmHg"],
                    "unit": "mmHg",
                    "system": "http://unitsofmeasure.org",
                    "code": "mm[Hg]"
                }
            }
        ]
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse OpenEHR blood pressure data")
    parser.add_argument("filename", nargs="?", default="bp_openehr.json", help="Input JSON file")
    parser.add_argument("--to-fhir", action="store_true", help="Output as FHIR R4 Observation JSON")
    args = parser.parse_args()

    try:
        obs = load_observation(args.filename)
        if args.to_fhir:
            print(json.dumps(to_fhir_observation(obs), indent=2))
        else:
            print_blood_pressure(obs)
    except FileNotFoundError:
        print(f"Error: File '{args.filename}' not found.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{args.filename}': {e}", file=sys.stderr)
        sys.exit(1)
    except KeyError as e:
        print(f"Error: Missing field {e} in JSON data.", file=sys.stderr)
        sys.exit(1)
