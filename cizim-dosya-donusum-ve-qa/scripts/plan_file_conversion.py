#!/usr/bin/env python3
import argparse
import json
import shutil
from pathlib import Path


KIND_BY_EXT = {
    ".dwg": "cad_dwg",
    ".dxf": "cad_dxf",
    ".ifc": "bim_ifc",
    ".ifczip": "bim_ifczip",
    ".rvt": "bim_revit_proprietary",
    ".skp": "sketchup_proprietary",
    ".pdf": "pdf",
    ".svg": "vector_svg",
    ".png": "raster_image",
    ".jpg": "raster_image",
    ".jpeg": "raster_image",
    ".tif": "raster_image",
    ".tiff": "raster_image",
    ".webp": "raster_image",
    ".obj": "mesh_3d",
    ".fbx": "mesh_3d",
    ".dae": "mesh_3d",
    ".stl": "mesh_3d",
    ".3mf": "mesh_3d",
    ".glb": "gltf",
    ".gltf": "gltf",
    ".step": "solid_cad",
    ".stp": "solid_cad",
    ".iges": "solid_cad",
    ".igs": "solid_cad",
    ".brep": "solid_cad",
    ".kml": "gis_vector",
    ".geojson": "gis_vector",
    ".gpkg": "gis_vector",
}


def tool(name):
    return shutil.which(name)


def route_for(kind, target, input_path, output_dir):
    ext = target.lower().lstrip(".")
    target = ext
    out = str(Path(output_dir) / f"{Path(input_path).stem}.{ext}") if target else None
    commands = []
    flags = []
    route = []

    if kind == "cad_dwg":
        route = ["Try LibreDWG for DWG decoding.", "Convert to DXF first, then run DXF QA."]
        if target == "dxf" and tool("dwg2dxf"):
            commands.append(f'"{tool("dwg2dxf")}" "{input_path}" -o "{out}"')
        else:
            flags.append("dwg_conversion_needs_libredwg_or_source_cad_export")
    elif kind == "cad_dxf":
        route = ["Inspect DXF entities/layers.", "Render/export with ezdxf or LibreCAD.", "Verify scale, font, hatch, lineweight."]
        if target in {"svg", "pdf", "png"} and tool("ezdxf"):
            commands.append(f'"{tool("ezdxf")}" draw -o "{out}" "{input_path}"')
        elif target:
            flags.append("dxf_export_tool_not_found")
    elif kind == "bim_ifc":
        route = ["Use IfcConvert for neutral geometry export.", "Check units, large coordinates, element count, and property loss."]
        converter = tool("IfcConvert") or tool("ifcconvert")
        if converter and target:
            commands.append(f'"{converter}" "{input_path}" "{out}"')
        else:
            flags.append("ifcconvert_not_found")
    elif kind == "solid_cad":
        route = ["Use FreeCADCmd or OCCT-based converter for solid CAD.", "Choose tessellation settings if exporting mesh.", "Verify units and topology."]
        converter = tool("FreeCADCmd") or tool("freecadcmd")
        if converter:
            commands.append("Use a FreeCAD Python macro to import source and export target format.")
        else:
            flags.append("freecad_or_occt_converter_not_found")
    elif kind in {"mesh_3d", "gltf"}:
        route = ["Use Assimp or Blender for mesh conversion.", "Run mesh/material/texture QA.", "Run glTF Validator for GLB/GLTF outputs."]
        if tool("assimp") and target:
            commands.append(f'"{tool("assimp")}" export "{input_path}" "{out}"')
        elif tool("blender"):
            commands.append("Use Blender background Python import/export route.")
        else:
            flags.append("mesh_converter_not_found")
    elif kind == "pdf":
        route = ["Use qpdf for structure checks.", "Use MuPDF/Poppler for raster pages.", "Record DPI and vector-to-raster risk."]
        if target in {"png", "jpg", "jpeg", "tiff"}:
            if tool("mutool"):
                commands.append(f'"{tool("mutool")}" draw -r 200 -o "{Path(output_dir) / (Path(input_path).stem + "-%03d." + ext)}" "{input_path}"')
            elif tool("pdftoppm"):
                commands.append(f'"{tool("pdftoppm")}" -r 200 -png "{input_path}" "{Path(output_dir) / Path(input_path).stem}"')
            else:
                flags.append("pdf_rasterizer_not_found")
        elif tool("qpdf"):
            commands.append(f'"{tool("qpdf")}" --check "{input_path}"')
    elif kind == "vector_svg":
        route = ["Use Inkscape for SVG export.", "Check fonts, page size, and rasterized effects."]
        if tool("inkscape") and target:
            commands.append(f'"{tool("inkscape")}" "{input_path}" --export-filename="{out}"')
        else:
            flags.append("inkscape_not_found")
    elif kind == "raster_image":
        route = ["Use ImageMagick for raster conversion.", "Check DPI, dimensions, color profile, and compression."]
        if tool("magick") and target:
            commands.append(f'"{tool("magick")}" "{input_path}" "{out}"')
        else:
            flags.append("imagemagick_not_found")
    elif kind == "gis_vector":
        route = ["Use GDAL/OGR for geospatial/vector conversion.", "Check CRS, geometry type, and coordinate precision."]
        if tool("ogr2ogr") and target:
            commands.append(f'"{tool("ogr2ogr")}" "{out}" "{input_path}"')
        else:
            flags.append("gdal_ogr_not_found")
    elif kind in {"bim_revit_proprietary", "sketchup_proprietary"}:
        route = ["Export from the source desktop application to IFC/DXF/OBJ/FBX/GLB first.", "Then run this skill on the neutral output."]
        flags.append("proprietary_source_format_requires_native_export")
    else:
        route = ["Unknown extension; inspect file magic and choose a conservative route."]
        flags.append("unknown_format")

    return {
        "kind": kind,
        "target": target,
        "output": out,
        "recommended_route": route,
        "commands_to_review": commands,
        "preflight_flags": flags,
        "post_conversion_qa": [
            "output_exists_and_nonzero",
            "input_output_hashes_recorded",
            "scale_or_dpi_verified",
            "geometry_or_page_count_compared",
            "losses_and_assumptions_reported",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description="Plan safe drawing/model file conversion routes.")
    parser.add_argument("--input", action="append", required=True)
    parser.add_argument("--target", required=True, help="Target extension, e.g. dxf, glb, png")
    parser.add_argument("--output-dir", default="conversion-output")
    args = parser.parse_args()

    plans = []
    for item in args.input:
        ext = Path(item).suffix.lower()
        kind = KIND_BY_EXT.get(ext, "unknown")
        plans.append({"input": item, **route_for(kind, args.target.lower().lstrip("."), item, args.output_dir)})

    print(json.dumps({"plans": plans}, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
