import os
from lib.database import Database

this_dir = os.path.dirname(os.path.realpath(__file__))

# https://levlaz.org/sqlite-db-migrations-with-pragma-user_version/


def get_script_version(path):
    return int(path.split('_')[0])


def migrate(migrations_dir=f'{this_dir}/migrations'):
    database = Database()

    current_version = database.conn.cursor().execute(
        'pragma user_version').fetchone()[0]

    migration_files = list(os.listdir(migrations_dir))
    for migration_name in sorted(migration_files):
        migration_version = get_script_version(migration_name)

        if migration_version > current_version:
            print(f"applying migration {migration_name}")
            with open(f'{migrations_dir}/{migration_name}', mode='r') as migration_file:
                database.conn.cursor().executescript(migration_file.read())
                print(f"database now at version {migration_version}")
        else:
            print(f"migration {migration_name} already applied")


if __name__ == "__main__":
    migrate()
