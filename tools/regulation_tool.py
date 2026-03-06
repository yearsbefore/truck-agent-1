import re
from langchain.tools import tool

# Structured regulation data (numeric limits for precise queries)
# Units: length in meters, weight in tons
REGULATIONS = {
    "EU": {
        "name": "EU Regulation (Directive 96/53/EC)",
        "max_length_m": 18.75,
        "max_width_m": 2.55,
        "max_height_m": 4.0,
        "max_weight_ton": 40.0,
        "notes": "Refrigerated vehicles may have width up to 2.60m. Some member states allow higher gross weights."
    },
    "US": {
        "name": "US Federal Regulation (FHWA Federal Size Regulations)",
        "max_length_m": 20.12,
        "max_width_m": 2.59,
        "max_height_m": 4.11,
        "max_weight_ton": 36.29,
        "notes": "Individual states may impose additional restrictions. Interstate highway limits may differ from local roads."
    },
    "CN": {
        "name": "China Regulation (GB 1589-2016)",
        "max_length_m": 18.1,
        "max_width_m": 2.55,
        "max_height_m": 4.0,
        "max_weight_ton": 49.0,
        "notes": "Semi-trailer train total length must not exceed 18.1m. Gross weight includes cargo."
    },
    "UK": {
        "name": "UK Regulation (Road Vehicles Regulations 1986)",
        "max_length_m": 18.75,
        "max_width_m": 2.55,
        "max_height_m": 4.2,
        "max_weight_ton": 44.0,
        "notes": "Post-Brexit UK regulations largely align with EU, but some details differ."
    },
}


def _parse_truck_spec(truck_spec: str) -> dict:
    """
    Extract truck parameters from natural language description.
    Example: "length 17m height 3.8m width 2.5m weight 38 tons"
    Returns: {"length": 17.0, "height": 3.8, "width": 2.5, "weight": 38.0}
    """
    spec = {}

    length_match = re.search(r'(?:length|\u957f\u5ea6)\s*[:=]?\s*([\d.]+)\s*(?:m|\u7c73)?', truck_spec, re.IGNORECASE)
    if length_match:
        spec["length"] = float(length_match.group(1))

    width_match = re.search(r'(?:width|\u5bbd\u5ea6)\s*[:=]?\s*([\d.]+)\s*(?:m|\u7c73)?', truck_spec, re.IGNORECASE)
    if width_match:
        spec["width"] = float(width_match.group(1))

    height_match = re.search(r'(?:height|\u9ad8\u5ea6)\s*[:=]?\s*([\d.]+)\s*(?:m|\u7c73)?', truck_spec, re.IGNORECASE)
    if height_match:
        spec["height"] = float(height_match.group(1))

    weight_match = re.search(r'(?:weight|\u91cd\u91cf)\s*[:=]?\s*([\d.]+)\s*(?:ton|tons|t|\u5428)\b', truck_spec, re.IGNORECASE)
    if weight_match:
        spec["weight"] = float(weight_match.group(1))

    return spec


def _check_single_region(spec: dict, region_key: str) -> str:
    """Check compliance for a single region and return a report."""
    reg = REGULATIONS[region_key]
    issues = []
    passes = []

    checks = [
        ("length", "max_length_m", "Length"),
        ("width",  "max_width_m",  "Width"),
        ("height", "max_height_m", "Height"),
        ("weight", "max_weight_ton", "Gross Weight"),
    ]

    for spec_key, reg_key, label in checks:
        if spec_key in spec:
            value = spec[spec_key]
            limit = reg[reg_key]
            unit = "tons" if spec_key == "weight" else "m"
            if value > limit:
                issues.append(f"  FAIL {label}: {value}{unit} > limit {limit}{unit} (exceeds by {round(value - limit, 2)}{unit})")
            else:
                passes.append(f"  PASS {label}: {value}{unit} <= limit {limit}{unit}")

    result = f"\n[{reg['name']}]\n"
    result += "\n".join(passes + issues)
    if reg.get("notes"):
        result += f"\n  NOTE: {reg['notes']}"

    if issues:
        result += f"\n  => Result: NON-COMPLIANT. {len(issues)} item(s) exceeded limits."
    elif passes:
        result += f"\n  => Result: COMPLIANT. All {len(passes)} item(s) passed."
    else:
        result += "\n  => Insufficient parameters provided for verification."

    return result


@tool
def check_regulations(truck_spec: str, region: str = "AUTO") -> str:
    """
    Check whether a truck complies with regulations for a specified region (dimensions and weight).
    truck_spec: Truck specification string, e.g. "length 17m height 3.8m width 2.5m weight 38 tons"
    region: Region code - EU, US, CN, UK. Enter ALL to check all regions, or AUTO to infer from text.
    Example: check_regulations("length 17m height 3.8m width 2.5m weight 38 tons", "EU")
    """
    region = (region or "AUTO").strip().upper()

    spec = _parse_truck_spec(truck_spec)
    if not spec:
        return (
            "Could not extract truck parameters from the description. Please use this format:\n"
            "Example: 'length 17m height 3.8m width 2.5m weight 38 tons'"
        )

    if region == "AUTO":
        text = truck_spec.upper()
        if any(k in text for k in ["EU", "EUROPE", "\u6b27\u6d32"]):
            regions_to_check = ["EU"]
        elif any(k in text for k in ["US", "USA", "AMERICA", "\u7f8e\u56fd"]):
            regions_to_check = ["US"]
        elif any(k in text for k in ["CN", "CHINA", "\u4e2d\u56fd"]):
            regions_to_check = ["CN"]
        elif any(k in text for k in ["UK", "BRITAIN", "ENGLAND", "\u82f1\u56fd"]):
            regions_to_check = ["UK"]
        else:
            regions_to_check = list(REGULATIONS.keys())
    elif region == "ALL":
        regions_to_check = list(REGULATIONS.keys())
    elif region in REGULATIONS:
        regions_to_check = [region]
    else:
        supported = ", ".join(REGULATIONS.keys())
        return f"Unsupported region code: {region}. Supported regions: {supported}, or enter ALL to check all."

    report = f"Truck Compliance Report\n"
    report += f"Specifications: {truck_spec}\n"
    report += "=" * 40

    for r in regions_to_check:
        report += _check_single_region(spec, r)
        report += "\n" + "-" * 40

    return report
