import duckdb
from gramex.transforms import handler

def clean_url(url):
    """
    Cleans a URL by replacing:
    - '%20' with a space
    - '%' with a space
    - '+' with a space
    - Removes '.html' extension
    """
    if not url:
        return url
    return url.replace('%20', ' ').replace('%', ' ').replace('+', ' ').replace('.html', '')


def get_most_used():
    # Create leaderboard_stats directory if it doesn't exist
    import os
    from datetime import 
    
    os.makedirs('leaderboard_stats', exist_ok=True)
    
    # Use single database file for both apps and templates
    db_path = os.path.join('leaderboard_stats', 'leaderboard.db')
    
    # Get current date for database entries
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Log file path
    log_file_path = './var/logs/nginx/access.llmfoundry.log
    
    # Call the functions with the new path and current date
    get_apps(db_path, current_date, log_file_path)
    get_templates(db_path, current_date, log_file_path)

def get_apps(db_path, current_date, log_file_path):
    # Connect to DuckDB
    conn_duckdb = duckdb.connect(database=':memory:', read_only=False)

    try:
        # Create a table for the log data using read_csv_auto
        conn_duckdb.execute(f"""
        CREATE TABLE access_logs AS
        SELECT *
        FROM read_csv_auto('{log_file_path}', columns={{
        'ip': 'VARCHAR',
        'ts': 'VARCHAR',
        'status': 'INTEGER',
        'bytes': 'INTEGER',
        'duration': 'DOUBLE',
        'upstream': 'VARCHAR',
        'request_line': 'VARCHAR',
        'field8': 'VARCHAR',
        'user_agent': 'VARCHAR',
        'field10': 'VARCHAR',
        'field11': 'VARCHAR'
        }});
        """)

        # Query for top apps
        query_apps = """
        SELECT 
            trim('/apps/' FROM url) AS raw_url, 
            COUNT(*) AS request_count
        FROM (SELECT split_part(trim(both '"' from request_line), ' ', 2) AS url FROM access_logs) sub
        WHERE url LIKE '/apps/%'
        GROUP BY raw_url
        ORDER BY request_count DESC
        LIMIT 30;
        """
        apps_result = conn_duckdb.execute(query_apps).fetchall()
        cleaned_apps_result = [(clean_url(row[0]), row[1]) for row in apps_result]
        # SQLite connection for both tables
        sqlite_conn = sqlite3.connect(db_path)
        cursor = sqlite_conn.cursor()

        # Create apps table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS top_apps (
            app_name TEXT,
            request_count INTEGER,
            date TEXT,
            PRIMARY KEY (app_name, date)
        );
        ''')

        # Delete existing entries for current date only
        cursor.execute('DELETE FROM top_apps WHERE date = ?;', (current_date,))
        
        # Insert cleaned top apps results into SQLite with date
        cursor.executemany('''
        INSERT INTO top_apps (app_name, request_count, date)
        VALUES (?, ?, ?);
        ''', [(app, count, current_date) for app, count in cleaned_apps_result])

        sqlite_conn.commit()
        sqlite_conn.close()
    finally
        conn_duckdb.close()

def get_templates(db_path, current_date, log_file_path):
    # Connect to DuckDB
    conn_duckdb = duckdb.connect(database=':memory:', read_only=False)

    try:
        # Create a table for the log data using read_csv_auto
        conn_duckdb.execute(f"""
        CREATE TABLE access_logs AS
        SELECT *
        FROM read_csv_auto('{log_file_path}', columns={{
        'ip': 'VARCHAR',
        'ts': 'VARCHAR',
        'status': 'INTEGER',
        'bytes': 'INTEGER',
        'duration': 'DOUBLE',
        'upstream': 'VARCHAR',
        'request_line': 'VARCHAR',
        'field8': 'VARCHAR',
        'user_agent': 'VARCHAR',
        'field10': 'VARCHAR',
        'field11': 'VARCHAR'
        }})
        """)

        # Query for top templates
        query_templates = """
        SELECT 
            split_part(split_part(url, '?id=', 2), '&', 1) AS raw_template_name, 
            COUNT(*) AS request_count
        FROM (SELECT split_part(trim(both '"' from request_line), ' ', 2) AS url FROM access_logs) sub
        WHERE url LIKE '/-/templates?id=%'
        GROUP BY raw_template_name
        ORDER BY request_count DESC
        LIMIT 30
        """
        templates_result = conn_duckdb.execute(query_templates).fetchall()
        cleaned_templates_result = [(clean_url(row[0]), row[1]) for row in templates_result]

        # SQLite connection for both tables
        sqlite_conn = sqlite3.connect(db_path)
        cursor = sqlite_conn.cursor()

        # Create templates table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS top_templates (
            template_name TEXT,
            request_count INTEGER,
            date TEXT,
            PRIMARY KEY (template_name, date)
        );
        ''')

        # Delete existing entries for current date only
        cursor.execute(DELETE FROM top_templates WHERE date = ?;', (current_date,))

        # Insert cleaned top templates results into SQLite with date
        cursor.executemany('''
        INSERT INTO top_templates (template_name, request_count, date)
        VALUES (?, ?, ?);
        ''', [(template, count, current_date) for template, count in cleaned_templates_result]

        sqlite_conn.commit()
        sqlite_conn.close()
        conn_duckdb.close()
