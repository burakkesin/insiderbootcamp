import mysql.connector

# Establish connection to MySQL database
connection = mysql.connector.connect(
    host='your_host',
    user='root',
    password='burak13579',
    database='your_database'
)

def save_test_result(test_name, passed, error_message=None):
    try:
        # Create cursor
        cursor = connection.cursor()

        # Define the MySQL insert statement
        insert_statement = "INSERT INTO test_results (test_name, passed, error_message) VALUES (%s, %s, %s)"

        # Execute the insert statement
        cursor.execute(insert_statement, (test_name, passed, error_message))

        # Commit the transaction
        connection.commit()

        print("Test result saved successfully to MySQL database")

    except mysql.connector.Error as error:
        print("Error while saving test result to MySQL:", error)

def test_verify_homepage_accessibility(driver, homepage_url):
    test_name = "test_verify_homepage_accessibility"
    try:
        driver.get(homepage_url)
        assert "Insider" in driver.title  # Check if the homepage title contains "Insider"
        save_test_result(test_name, passed=True)
    except AssertionError as e:
        save_test_result(test_name, passed=False, error_message=str(e))
        raise e

def test_navigate_to_careers_page(driver, homepage_url, careers_page_url):
    test_name = "test_navigate_to_careers_page"
    try:
        driver.get(homepage_url)
        # Navigate to Careers page
        # your test code...

        save_test_result(test_name, passed=True)
    except Exception as e:
        save_test_result(test_name, passed=False, error_message=str(e))
        raise e

# Define other test functions similarly...

# Close the connection after all tests are done
connection.close()
