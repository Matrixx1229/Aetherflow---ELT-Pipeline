import subprocess
import time
import os

# --- Configuration ---
source_config = {
    'dbname': "source_db",
    'user': "postgres",
    'password': "secret",
    'host': "source_postgres",  # Make sure this matches your docker-compose service name
}

destination_config = {
    'dbname': "destination_db",      # CHANGED: standard default DB name
    'user': "postgres",
    'password': "secret",
    # Make sure this matches your docker-compose service name
    'host': "destination_postgres",
}


def wait_for_postgres(host, max_retries=5, wait_seconds=5):
    """Wait for PostgreSQL to be ready."""
    retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host],
                check=True,
                capture_output=True,
                text=True
            )
            if "accepting connections" in result.stdout:
                print(f"Successfully connected to {host}.")
                return True
        except subprocess.CalledProcessError as e:
            print(
                f"Waiting for {host}... (Attempt {retries + 1}/{max_retries})")
            time.sleep(wait_seconds)
            retries += 1

    print(f"Max retries reached for {host}. Exiting.")
    return False


print("Starting ELT Script...")

# --- 1. Wait for BOTH databases ---
if not wait_for_postgres(source_config['host']):
    exit(1)

if not wait_for_postgres(destination_config['host']):  # ADDED this check
    exit(1)

# --- 2. Dump from Source ---
print("Dumping data from source...")
dump_command = [
    'pg_dump',
    '-h', source_config['host'],
    '-U', source_config['user'],
    '-d', source_config['dbname'],
    '-f', 'data_dump.sql',
    '-w'
]

# Use os.environ to keep other env vars
subprocess_env_source = dict(os.environ, PGPASSWORD=source_config['password'])
subprocess.run(dump_command, env=subprocess_env_source, check=True)

# --- 3. Load into Destination ---
print("Loading data into destination...")
load_command = [
    'psql',
    '-h', destination_config['host'],
    '-U', destination_config['user'],
    '-d', destination_config['dbname'],
    '-a', '-f', 'data_dump.sql'
]

subprocess_env_dest = dict(
    os.environ, PGPASSWORD=destination_config['password'])
subprocess.run(load_command, env=subprocess_env_dest, check=True)

print("ELT script finished successfully.")
