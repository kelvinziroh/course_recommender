-- Create the database
CREATE DATABASE IF NOT EXISTS CourseReviews;

-- Use the created database
USE CourseReviews;

-- Create the table
CREATE TABLE CourseReviews.course_reviews (
	id INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for each record
	course_name VARCHAR(255) NOT NULL,
	course_source VARCHAR(255) NOT NULL,
	course_rating FLOAT NOT NULL,
	course_review TEXT NOT NULL,
	sentiment VARCHAR(50) NOT NULL
);