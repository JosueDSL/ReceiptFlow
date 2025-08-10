Single-database configuration for Flask.

# How to Make a Database Migration with Flask

### Single-database configuration for Flask.

1. **Initialize the Migrations Directory:**
```bash
   flask db init
```


# How to Make a Database Migration with Flask

### Single-database configuration for Flask.

1. **Initialize the Migrations Directory:**
   ```bash
   flask db init
   ```

   This command will create a `migrations/` directory in your project, which will store migration files.

2. **Generate a New Migration:**
   ```bash
   flask db migrate -m "Commit message"
   ```

   This command scans the models for changes and generates a migration file with the necessary SQL to modify the database schema. Replace `"Commit message"` with a meaningful description of the changes.

3. **Apply the Migration:**
   ```bash
   flask db upgrade
   ```

   This command applies the generated migration file, updating your database schema to match the current state of your models.

By following these steps, you'll successfully apply the changes to your database schema.
