# db-to-zod

Generate TypeScript types and [Zod](https://zod.dev) schemas from SQL `CREATE TABLE` statements.

```bash
pip install db-to-zod
db-to-zod schema.sql -o schema.ts
```

**Input**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    full_name TEXT,
    created_at DATETIME NOT NULL
);
```

**Output**
```ts
import { z } from 'zod';

export const UsersSchema = z.object({
  id: z.number().int(),
  email: z.string(),
  full_name: z.string().nullable().optional(),
  created_at: z.string().datetime(),
});

export type Users = z.infer<typeof UsersSchema>;
```

## What it handles
- `CREATE TABLE [IF NOT EXISTS]` for SQLite / PostgreSQL / MySQL-style DDL
- Common types: INTEGER/INT/BIGINT, REAL/FLOAT/DOUBLE/NUMERIC, TEXT/VARCHAR/CHAR, BOOLEAN, DATETIME/TIMESTAMP, JSON, BLOB
- `NOT NULL` and `PRIMARY KEY` -> required; otherwise `.nullable().optional()`

## Limitations (v1)
- One column definition per line is expected
- No enums, arrays, `CHECK` constraints, defaults or foreign-key awareness
- Unknown types fall back to `z.string()`
- Reads `.sql` files only; it does not connect to a database

MIT licensed. Issues and PRs welcome.
