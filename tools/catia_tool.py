import os
import re
from langchain.tools import tool

# CATIA is controlled via COM interface using pywin32 (Windows only)
# Use mock mode during development; switch to real mode when CATIA is installed
CATIA_MODE = os.getenv("CATIA_MODE", "mock")  # "mock" or "real"


def _get_catia_app():
    """Get the CATIA COM object (real mode only)"""
    try:
        import win32com.client
        return win32com.client.Dispatch("CATIA.Application")
    except Exception as e:
        raise RuntimeError(f"Cannot connect to CATIA. Please ensure CATIA is running: {e}")


def _execute_catia_action(action: str, params: dict) -> str:
    """Execute a specific CATIA operation."""
    if action == "open_file":
        catia = _get_catia_app()
        catia.Documents.Open(params.get("file_path", ""))
        return f"Opened file: {params.get('file_path')}"

    elif action == "set_parameter":
        catia = _get_catia_app()
        doc = catia.ActiveDocument
        param_name = params.get("name")
        param_value = params.get("value")
        part = doc.Part
        parameters = part.Parameters
        param = parameters.GetItem(param_name)
        param.Value = float(param_value)
        part.Update()
        return f"Parameter {param_name} updated to {param_value}"

    elif action == "export_model":
        catia = _get_catia_app()
        doc = catia.ActiveDocument
        export_path = params.get("export_path", "output.stp")
        doc.ExportData(export_path, "stp")
        return f"Model exported to: {export_path}"

    elif action == "get_parameters":
        catia = _get_catia_app()
        doc = catia.ActiveDocument
        part = doc.Part
        params_list = []
        for i in range(1, part.Parameters.Count + 1):
            p = part.Parameters.Item(i)
            params_list.append(f"{p.Name} = {p.Value}")
        return "Current model parameters:\n" + "\n".join(params_list)

    else:
        return f"Unknown action type: {action}"


def _mock_catia_action(instruction: str) -> str:
    """Mock mode: simulate CATIA operations for development without CATIA installed."""
    return (
        f"[MOCK MODE] Simulated CATIA operation: {instruction}\n"
        f"To use real CATIA, set CATIA_MODE=real in .env and ensure CATIA is running."
    )


def _extract_open_path(instruction: str) -> str:
    match = re.search(r'([A-Za-z]:[\\/][^\s]+?\.(?:CATPart|CATProduct|stp|step|igs|iges))', instruction, re.IGNORECASE)
    return match.group(1) if match else ""


def _extract_set_parameter(instruction: str) -> tuple[str, str]:
    # Examples:
    # "Set parameter FRAME_LENGTH to 8000"
    # "change WHEEL_BASE = 7200"
    match = re.search(
        r'(?:set|modify|change)\s+(?:parameter\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*(?:to|=)\s*([-\d.]+)',
        instruction,
        re.IGNORECASE,
    )
    if not match:
        return "", ""
    return match.group(1), match.group(2)


def _extract_export_path(instruction: str) -> str:
    match = re.search(r'([A-Za-z]:[\\/][^\s]+?\.(?:stp|step|igs|iges))', instruction, re.IGNORECASE)
    return match.group(1) if match else "output.stp"


@tool
def control_catia_software(instruction: str) -> str:
    """
    Control CATIA modeling software.
    Supports: opening model files, modifying parameters, exporting models, viewing parameters.
    Example input:
      - "Open file C:/models/truck_chassis.CATPart"
      - "Set parameter FRAME_LENGTH to 8000mm"
      - "Export current model as STEP to C:/output/model.stp"
      - "Show all current model parameters"
    """
    if CATIA_MODE == "mock":
        return _mock_catia_action(instruction)

    instruction_lower = instruction.lower()
    try:
        if "open" in instruction_lower:
            file_path = _extract_open_path(instruction)
            if not file_path:
                return "Open action detected, but no valid file path was found."
            return _execute_catia_action("open_file", {"file_path": file_path})

        elif "set" in instruction_lower or "modify" in instruction_lower or "change" in instruction_lower:
            param_name, param_value = _extract_set_parameter(instruction)
            if not param_name:
                return "Set action detected, but parameter name/value could not be parsed."
            return _execute_catia_action("set_parameter", {
                "name": param_name,
                "value": param_value,
            })

        elif "export" in instruction_lower:
            export_path = _extract_export_path(instruction)
            return _execute_catia_action("export_model", {"export_path": export_path})

        elif "show" in instruction_lower or "parameter" in instruction_lower:
            return _execute_catia_action("get_parameters", {})

        else:
            return f"Could not identify action type. Please be more specific. Received: {instruction}"

    except Exception as e:
        return f"CATIA operation failed: {str(e)}"
