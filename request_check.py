EXPECTED_UNITS = {
    "m_dot": "kg/s",
    "t_in": "K",
    "p_in": "bar",
    "p_out": "bar",
    "k": "dimensionless",
    "r_gas": "J/(kg*K)",
    "eta": "dimensionless",
}


def check_units(request):
    for name, expected_unit in EXPECTED_UNITS.items():
        if name not in request["inputs"]:
            raise ValueError(f"Missing input: {name}")
        unit = request["inputs"][name]["unit"]
        if unit != expected_unit:
            raise ValueError(f"{name}: expected unit {expected_unit}, got {unit}")


request = {
    "action": "run_compressor",
    "pressure_basis": "absolute",
    "inputs": {
    "m_dot":  { "value": 0.10,  "unit": "kg/s" },
    "t_in":   { "value": 300.0, "unit": "K" },
    "p_in":   { "value": 1.0,   "unit": "bar" },
    "p_out":  { "value": 8.0,   "unit": "bar" },
    "k":      { "value": 1.4,   "unit": "dimensionless" },
    "r_gas":  { "value": 287.0, "unit": "J/(kg*K)" },
    "eta":    { "value": 0.75,  "unit": "dimensionless" }
        # type the seven inputs here from your AI_DESIGN.md
    },
    "report": ["power"],
}
check_units(request)
print("units ok")