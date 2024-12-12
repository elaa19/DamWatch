<?php
// Enable error reporting for debugging
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Connection details
$host = "localhost";
$port = "5432"; // Default PostgreSQL port
$dbname = "DamWatch"; // Your database name
$user = "postgres"; // Your PostgreSQL username
$password = "nadagouja"; // Your password

// Establish the connection
$conn = pg_connect("host=$host port=$port dbname=$dbname user=$user password=$password");

if (!$conn) {
    die("Error in connection: " . pg_last_error());
}

// Handle registration (POST request)
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['name']) && isset($_POST['email']) && isset($_POST['password'])) {
    // Get and escape the form data to prevent SQL injection
    $name = pg_escape_string($conn, $_POST['name']);
    $email = pg_escape_string($conn, $_POST['email']);
    $password = $_POST['password'];

    // Check if password length exceeds 20 characters
    if (strlen($password) > 20) {
        echo "Password cannot exceed 20 characters.";
    } else {
        // Check if the email already exists
        $check_query = "SELECT * FROM Registration WHERE email = '$email'";
        $check_result = pg_query($conn, $check_query);

        if (pg_num_rows($check_result) > 0) {
            // Email already exists, show an error message
            echo "<script>alert('This email is already registered. Please use a different email.');</script>";
        } else {
            // SQL query to insert data (storing password as plain text)
            $query = "INSERT INTO Registration (name, email, password) VALUES ('$name', '$email', '$password')";

            // Execute the query
            $result = pg_query($conn, $query);

            if ($result) {
                echo "Registration successful!";
            } else {
                echo "Error: " . pg_last_error($conn);
            }
        }
    }
}


// Handle login (GET request)
if ($_SERVER["REQUEST_METHOD"] == "GET" && isset($_GET['email']) && isset($_GET['password'])) {
    // Get the form data
    $email = pg_escape_string($conn, $_GET['email']);
    $password = $_GET['password'];

    // Query to check if the email exists
    $query = "SELECT * FROM Registration WHERE email = '$email'";
    $result = pg_query($conn, $query);

    // Check if user exists
    if (pg_num_rows($result) == 1) {
        $row = pg_fetch_assoc($result);

        // Check if the entered password matches the stored password
        if ($password === $row['password']) {
            // Redirect to map.html if login is successful
            header("Location: map.html");
            exit();
        } else {
            // Error message if password does not match
            echo "<script>alert('Incorrect password! Please try again.');</script>";
        }
    } else {
        // Error message if email is not found
        echo "<script>alert('Email not registered or invalid. Please check and try again.');</script>";
    }
}

// Close the connection
pg_close($conn);
?>
