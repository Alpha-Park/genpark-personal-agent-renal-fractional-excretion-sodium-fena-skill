"""
MCP Server for Renal Fractional Excretion of Sodium (FeNa) & Urea Skill.
Conforms to Model Context Protocol (MCP) JSON-RPC 2.0 stdio specification.
"""

import sys
import json
from client import RenalFractionalExcretionClient


def handle_request(line: str) -> None:
    try:
        req = json.loads(line)
    except Exception:
        return

    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "genpark-personal-agent-renal-fractional-excretion-sodium-fena-skill",
                    "version": "1.0.0"
                }
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/list":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "evaluate_excretion",
                        "description": "Calculate Fractional Excretion of Sodium (FeNa), FeUrea, and renal hydration index.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "urine_sodium_mmol_l": {"type": "number", "description": "Spot urine sodium (mmol/L)."},
                                "plasma_sodium_mmol_l": {"type": "number", "description": "Serum/plasma sodium (mmol/L)."},
                                "urine_creatinine_mg_dl": {"type": "number", "description": "Urine creatinine (mg/dL)."},
                                "plasma_creatinine_mg_dl": {"type": "number", "description": "Serum/plasma creatinine (mg/dL)."},
                                "urine_urea_mg_dl": {"type": "number", "description": "Urine urea nitrogen (mg/dL, optional)."},
                                "plasma_urea_nitrogen_mg_dl": {"type": "number", "description": "Blood urea nitrogen BUN (mg/dL, optional)."},
                                "on_diuretics": {"type": "boolean", "description": "Whether patient is on diuretic medications."}
                            },
                            "required": [
                                "urine_sodium_mmol_l",
                                "plasma_sodium_mmol_l",
                                "urine_creatinine_mg_dl",
                                "plasma_creatinine_mg_dl"
                            ]
                        }
                    }
                ]
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "evaluate_excretion":
            client = RenalFractionalExcretionClient()
            try:
                res = client.evaluate_excretion(
                    urine_sodium_mmol_l=float(args["urine_sodium_mmol_l"]),
                    plasma_sodium_mmol_l=float(args["plasma_sodium_mmol_l"]),
                    urine_creatinine_mg_dl=float(args["urine_creatinine_mg_dl"]),
                    plasma_creatinine_mg_dl=float(args["plasma_creatinine_mg_dl"]),
                    urine_urea_mg_dl=float(args["urine_urea_mg_dl"]) if "urine_urea_mg_dl" in args and args["urine_urea_mg_dl"] is not None else None,
                    plasma_urea_nitrogen_mg_dl=float(args["plasma_urea_nitrogen_mg_dl"]) if "plasma_urea_nitrogen_mg_dl" in args and args["plasma_urea_nitrogen_mg_dl"] is not None else None,
                    on_diuretics=bool(args.get("on_diuretics", False))
                )
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    }
                }
            except Exception as e:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                }
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
    else:
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method {method} not found"}
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()


def main():
    for line in sys.stdin:
        if line.strip():
            handle_request(line)


if __name__ == "__main__":
    main()
