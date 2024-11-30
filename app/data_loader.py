import json
import pandas as pd
import mysql.connector

def extract_reviews():
    """Extract the course reviews from the database

    Returns:
        pandas.core.frame.DataFrame: A dataframe object of the course reviews retrieved from the database
    """
    # Load db connector details from the configuration file
    with open("../assets/scripts/df_config.json") as config_file:
        config = json.load(config_file)
    
    # Create a mysql connection
    mydb = mysql.connector.connect(
        host = config["host"],
        user = config["user"],
        password = config["password"],
        database = config["database"]
    )

    # Create a cursor object
    mycursor = mydb.cursor()

    # SQL query all records from the course_reviews table
    sql = "SELECT * FROM course_reviews;"

    # Execute the query
    mycursor.execute(sql)

    # Fetch all the rows from the query's result
    rows = mycursor.fetchall()

    # Fetch all the column names
    column_names = [desc[0] for desc in mycursor.description]

    # Create a dataframe from all the fetched data
    loaded_df = pd.DataFrame(rows, columns=column_names)
    
    # Close the cursor and connection
    mycursor.close()
    mydb.close()
    
    return loaded_df