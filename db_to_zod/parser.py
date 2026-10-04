import re
from typing import Any, Dict, List, Tuple

SQL_TYPE_MAP = {
    "INTEGER": ("z.number().int()", "number"),
    "INT": ("z.number().int()", "number"),
    "BIGINT": ("z.number().int()", "number"),
    "REAL": ("z.number()", "number"),
    "FLOAT": ("z.number()", "number"),
    "DOUBLE": ("z.number()", "number"),
    "NUMERIC": ("z.number()", "number"),
    "TEXT": ("z.string()", "string"),
    "VARCHAR": ("z.string()", "string"),
    "CHAR": ("z.string()", "string"),
    "BOOLEAN": ("z.boolean()", "boolean"),
    "DATETIME": ("z.string().datetime()", "string"),
    "TIMESTAMP": ("z.string().datetime()", "string"),
    "JSON": ("z.record(z.any())", "Record<string, any>"),
    "BLOB": ("z.instanceof(Uint8Array)", "Uint8Array")
}

def parse_sql_ddl(sql_text: str) -> List[Dict[str, Any]]:
    tables = []
    # Match CREATE TABLE tableName (...)
    table_matches = re.finditer(r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([a-zA-Z0-9_]+)\s*\((.*?)\);", sql_text, re.DOTALL | re.IGNORECASE)
    
    for tm in table_matches:
        table_name = tm.group(1)
        body = tm.group(2)
        columns = []
        
        lines = [line.strip().rstrip(",") for line in body.split("\n") if line.strip()]
        for line in lines:
            if line.upper().startswith(("PRIMARY KEY", "FOREIGN KEY", "CONSTRAINT", "UNIQUE")):
                continue
            parts = line.split()
            if len(parts) >= 2:
                col_name = parts[0].strip('"`[]')
                raw_type = parts[1].upper().split("(")[0]
                is_nullable = "NOT NULL" not in line.upper() and "PRIMARY KEY" not in line.upper()
                
                zod_type, ts_type = SQL_TYPE_MAP.get(raw_type, ("z.string()", "string"))
                if is_nullable:
                    zod_type += ".nullable().optional()"
                    ts_type += " | null"
                    
                columns.append({
                    "name": col_name,
                    "zod": zod_type,
                    "ts": ts_type
                })
                
        tables.append({"name": table_name, "columns": columns})
    return tables

def generate_zod_schema(tables: List[Dict[str, Any]]) -> str:
    output = ["import { z } from 'zod';\n"]
    for t in tables:
        tname = t["name"]
        schema_name = f"{tname[0].upper()}{tname[1:]}Schema"
        type_name = f"{tname[0].upper()}{tname[1:]}"
        
        output.append(f"export const {schema_name} = z.object({{")
        for col in t["columns"]:
            output.append(f"  {col['name']}: {col['zod']},")
        output.append("});\n")
        output.append(f"export type {type_name} = z.infer<typeof {schema_name}>;\n")
    return "\n".join(output)
