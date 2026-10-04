import sys
import argparse
from pathlib import Path
from .parser import parse_sql_ddl, generate_zod_schema

def main():
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(errors="replace")
        except Exception:
            pass
    parser = argparse.ArgumentParser(description="db-to-zod: Generate TypeScript types & Zod schemas from SQL DDL.")
    parser.add_argument("schema", help="Path to schema.sql")
    parser.add_argument("-o", "--output", default="schema.ts", help="Destination TypeScript file")
    
    args = parser.parse_args()
    sql_path = Path(args.schema)
    if not sql_path.exists():
        print(f"❌ File not found: {sql_path}")
        return
        
    tables = parse_sql_ddl(sql_path.read_text(encoding="utf-8"))
    ts_code = generate_zod_schema(tables)
    
    out_file = Path(args.output)
    out_file.write_text(ts_code, encoding="utf-8")
    
    print(f"✨ Successfully generated Zod & TypeScript schemas!")
    print(f"• Tables parsed:  {len(tables)} tables")
    print(f"• Destination:    {out_file.resolve()}")

if __name__ == "__main__":
    main()
