#!/usr/bin/env python3
import argparse
import importlib.util
import json


ROUTES = {
    "quantity_takeoff": {
        "route": [
            "Normalize all dimensions to meters.",
            "Separate gross quantity, deductions, waste, and net quantity.",
            "Use basic_quantity_calculator.py or spreadsheet skill for table-heavy work.",
        ],
        "tools": ["basic_quantity_calculator.py", "spreadsheets"],
        "qa": ["units_present", "positive_dimensions", "openings_checked", "waste_separated"],
    },
    "unit_conversion": {
        "route": [
            "Use Pint if installed; otherwise use explicit stdlib conversion factors.",
            "Reject dimensionally inconsistent conversions.",
        ],
        "tools": ["pint", "manual_conversion_table"],
        "qa": ["source_unit_present", "target_unit_present", "dimension_compatible"],
    },
    "ifc_quantity": {
        "route": [
            "Use BIM skill to validate IFC model first.",
            "Use IfcOpenShell/Ifc5D for quantity extraction when installed.",
            "Compare model quantities with manual spot checks.",
        ],
        "tools": ["ifcopenshell", "ifc5d", "bim-revit-ifc-model-kontrolu"],
        "qa": ["ifc_schema_read", "quantity_sets_present", "spot_check_required"],
    },
    "section_properties": {
        "route": [
            "Use sectionproperties for arbitrary cross-section analysis.",
            "Use closed-form formulas only for simple rectangles/circles.",
            "Record units and coordinate axes.",
        ],
        "tools": ["sectionproperties", "sympy"],
        "qa": ["axes_defined", "units_present", "mesh_or_formula_documented"],
    },
    "reinforced_concrete_section": {
        "route": [
            "Use concreteproperties/structuralcodes only as calculation aids.",
            "Record code version, material model, reinforcement layout, and assumptions.",
            "Require licensed engineer review before design use.",
        ],
        "tools": ["concreteproperties", "structuralcodes"],
        "qa": ["code_version_recorded", "material_model_recorded", "engineer_review_required"],
    },
    "frame_analysis": {
        "route": [
            "Use anaStruct for 2D frame/truss pre-analysis or PyNite/Frame3DD for 3D elastic models.",
            "Record supports, loads, load combinations, section properties, and units.",
            "Treat output as analysis aid, not sealed design.",
        ],
        "tools": ["anastruct", "Pynite", "Frame3DD"],
        "qa": ["supports_recorded", "loads_recorded", "load_combinations_recorded", "engineer_review_required"],
    },
    "seismic_nonlinear": {
        "route": [
            "Use OpenSees/OpenSeesPy only with specialist modeling assumptions.",
            "Record material model, mass, damping, ground motion, solver settings, and convergence checks.",
            "Require expert review.",
        ],
        "tools": ["OpenSees", "openseespy"],
        "qa": ["expert_model_required", "convergence_checked", "engineer_review_required"],
    },
}


def module_exists(name):
    return importlib.util.find_spec(name) is not None


def main():
    parser = argparse.ArgumentParser(description="Plan construction calculation route.")
    parser.add_argument("--calculation-type", choices=sorted(ROUTES), default="quantity_takeoff")
    parser.add_argument("--input", action="append", default=[])
    args = parser.parse_args()

    selected = ROUTES[args.calculation_type]
    module_status = {
        name: module_exists(name)
        for name in ["pint", "sympy", "ifcopenshell", "ifc5d", "anastruct", "Pynite", "openseespy", "sectionproperties", "concreteproperties", "structuralcodes"]
    }
    result = {
        "calculation_type": args.calculation_type,
        "inputs": args.input,
        "recommended_route": selected["route"],
        "tools": selected["tools"],
        "qa_gates": selected["qa"],
        "available_python_modules": module_status,
        "approval_boundary": "Engineering design and code compliance require qualified professional review.",
    }
    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
