# OpenEHR Blood Pressure Parser

A Python utility that parses blood pressure observations from OpenEHR JSON format, validates the data, and can convert it to FHIR R4 Observation format.

## Features

- Parse blood pressure data from OpenEHR JSON format
- Validate required clinical parameters
- Display human-readable output with log-friendly summary
- Export to FHIR R4 Observation format with proper LOINC codes
- Zero external dependencies (Python standard library only)

## Requirements

- Python 3

## Usage

### Basic usage (human-readable output)

```bash
python parse_bp.py
```

Reads from default file `bp_openehr.json` and displays:

```
Blood pressure
Time: 2026-01-18T10:00:00Z
Sys: 132 mmHg
Dia: 84 mmHg
MAP: 100 mmHg
Pulse: 72 bpm
BP: 132/84 mmHg, MAP: 100 mmHg, Pulse: 72 bpm @ 2026-01-18T10:00:00Z
```

### Read from custom file

```bash
python parse_bp.py path/to/file.json
```

### Export to FHIR R4 format

```bash
python parse_bp.py --to-fhir
python parse_bp.py path/to/file.json --to-fhir
```

## Input Format

The script expects OpenEHR JSON with this structure:

```json
{
  "ehr_id": "example-ehr-1",
  "composition_uid": "example-comp-1",
  "observation": {
    "archetype_id": "openEHR-EHR-OBSERVATION.blood_pressure.v2",
    "time": "2026-01-18T10:00:00Z",
    "device": "Omron M3",
    "systolic_mmHg": 132,
    "diastolic_mmHg": 84,
    "mean_arterial_pressure_mmHg": 100,
    "pulse_per_min": 72,
    "position": "sitting",
    "location": "home"
  }
}
```

### Required fields in observation

- `time` - Timestamp of observation
- `systolic_mmHg` - Systolic pressure reading
- `diastolic_mmHg` - Diastolic pressure reading
- `mean_arterial_pressure_mmHg` - Mean arterial pressure
- `pulse_per_min` - Heart rate

## FHIR R4 Output

The `--to-fhir` option generates a valid FHIR R4 Observation resource with:

- Resource type: `Observation`
- Status: `final`
- Category: `vital-signs`
- LOINC codes:
  - `85354-9` - Blood pressure panel
  - `8480-6` - Systolic blood pressure
  - `8462-4` - Diastolic blood pressure
- Units: UCUM code `mm[Hg]`

## License

MIT
