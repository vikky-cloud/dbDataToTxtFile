import mysql.connector

# get db config info from user

def get_db_config():
    print("Enter your database configuration details:")
    user = input("Username: ")
    password = input("Password: ")
    host = input("Host: ")
    port = input("Port.No: ")
    database = input("Database name: ")
    
    return {
        'user': user,
        'password': password,
        'host': host,
        'port': port,
        'database': database
    }


# Show progress to user

def display_progress(current, total):
    percentage = (current / total) * 100
    print(f"Exporting data... {percentage:.2f}% complete.", end='\r')


# call the db cofig

config = get_db_config()


# try connecting to db with given config, if connection failed through exception

try:
    connection = mysql.connector.connect(**config)

    # create a cursor to interact with mentioned db
    cursor = connection.cursor()

    # get all the tables in the db
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    # create a file txt to export data from db

    output_file_name = f"{config['database']}_data.txt"
    with open(output_file_name, 'w') as file:

        #total count
        total_tables = len(tables)
        
        #iterate over each table
        for index, (table_name,) in enumerate(tables):

            # get the table data
            cursor.execute(f"SELECT * FROM {table_name}")
            table_data = cursor.fetchall()

            # write table name
            file.write(f"\n{table_name} Data:\n")
            
            # write column names
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = cursor.fetchall()
            column_names = [column[0] for column in columns]
            file.write(', '.join(column_names) + '\n')

            # write data rows
            for row in table_data:
                file.write(', '.join(map(str, row)) + '\n')

            # display status``
            display_progress(index + 1, total_tables)

    print(f"\nData exported successfully to {output_file_name}")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Close the cursor and connection if they were created
    if cursor:
        cursor.close()
    if connection:
        connection.close()
