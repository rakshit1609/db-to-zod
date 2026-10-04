# db-to-zod

Generate TypeScript + Zod schemas from SQL `CREATE TABLE` statements.

```bash
python -m src.cli schema.sql -o schema.ts
```

Input:
```sql
CREATE TABLE users (id INTEGER PRIMARY KEY, email VARCHAR(255) NOT NULL, full_name TEXT);
```
Output:
```ts
export const UsersSchema = z.object({ id: z.number().int(), email: z.string(), full_name: z.string().nullable().optional() });
export type Users = z.infer<typeof UsersSchema>;
```

Limitations: single-line column definitions, no enum/array/foreign-key awareness, unknown types fall back to `z.string()`.
