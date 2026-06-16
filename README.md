# AWS Music Subscription Platform

A portfolio-safe cloud music subscription web application built with a static HTML frontend, Flask REST API backend, and AWS DynamoDB for data storage.

This project demonstrates backend API development, cloud database integration, user authentication, subscription management, and portfolio-safe cloud configuration practices.

Project Status

Portfolio version completed and published for graduate/junior role applications.

This repository is a cleaned and rewritten public version. It does not include assignment briefs, private university documents, student IDs, hidden tests, credentials, protected starter code, or private datasets.

Project Overview

The AWS Music Subscription Platform allows users to register, log in, search for music records, subscribe to songs, view their saved subscriptions, and remove subscriptions.

The application is designed as a small full-stack cloud project showing how a static frontend can communicate with a Python Flask backend connected to AWS DynamoDB.

Problem Statement

Music platforms need a simple way for users to search music records and maintain a personalised subscription list.

This project solves that by providing:

User registration and login
Secure password hashing
Music search by title, artist, album, and year
Song subscription management
REST API endpoints for frontend communication
DynamoDB-backed persistence
Environment-based configuration for safer deployment
Key Features
User Management
User registration with email, username, and password
Login validation
Passwords stored using hashing instead of plain text
Email normalisation using lowercase formatting
Music Search
Search music by:
Title
Artist
Album
Year
Flexible filtering support
DynamoDB query and scan logic
Optional album-year index support for more efficient querying
Subscription Management
Add songs to a user subscription list
View saved subscriptions
Remove saved songs
Prevent duplicate subscriptions
Backend API
Flask REST API
JSON request and response handling
CORS configuration using environment variables
DynamoDB integration through boto3
Decimal conversion support for DynamoDB responses
Portfolio-Safe Cloud Practices
No hardcoded AWS keys
No hardcoded API Gateway endpoint
No hardcoded EC2 IP address
No hardcoded load balancer URL
AWS region and table names configurable through environment variables
Private academic files excluded from the public repository
Tech Stack
Frontend
HTML
CSS
JavaScript
Backend
Python
Flask
Flask-CORS
Werkzeug password hashing
boto3
Cloud and Database
AWS DynamoDB
AWS S3 static hosting concept
AWS API Gateway / EC2 / ECS deployment concept
AWS environment-based credentials
Tools
Git
GitHub
VS Code
Postman or browser-based API testing
Repository Structure
aws-music-subscription-platform/
│
├── app_backend.py
├── index.html
├── login.html
├── register.html
├── main.html
├── requirements.txt
├── .gitignore
└── README.md
Backend API Endpoints
Method	Endpoint	Description
GET	/	Health check endpoint
POST	/register	Register a new user
POST	/login	Log in an existing user
GET	/music	Search music records
GET	/subscribe	Get user subscriptions
POST	/subscribe	Add a song subscription
DELETE	/subscribe	Remove a song subscription
Example API Requests
Register
POST /register
Content-Type: application/json
{
  "email": "demo@example.com",
  "user_name": "Demo User",
  "password": "DemoPassword123"
}
Login
POST /login
Content-Type: application/json
{
  "email": "demo@example.com",
  "password": "DemoPassword123"
}
Search Music
GET /music?artist=Taylor%20Swift
Add Subscription
POST /subscribe
Content-Type: application/json
{
  "email": "demo@example.com",
  "title": "Love Story",
  "artist": "Taylor Swift",
  "album": "Fearless",
  "year": "2008",
  "image_url": "example-image-url"
}
Remove Subscription
DELETE /subscribe
Content-Type: application/json
{
  "email": "demo@example.com",
  "song_id": "Taylor Swift#Love Story#Fearless#2008"
}
Setup Instructions
1. Clone the Repository
git clone https://github.com/s4124147/aws-music-subscription-platform.git
cd aws-music-subscription-platform
2. Create a Virtual Environment
python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Activate it on macOS/Linux:

source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Configure Environment Variables

The backend uses environment variables instead of hardcoded cloud values.

Example Windows PowerShell setup:

$env:AWS_REGION = "us-east-1"
$env:LOGIN_TABLE_NAME = "login"
$env:MUSIC_TABLE_NAME = "music"
$env:SUBSCRIPTIONS_TABLE_NAME = "subscriptions"
$env:ALLOWED_ORIGINS = "http://localhost:5500,http://127.0.0.1:5500"
$env:PORT = "5000"

Example macOS/Linux setup:

export AWS_REGION="us-east-1"
export LOGIN_TABLE_NAME="login"
export MUSIC_TABLE_NAME="music"
export SUBSCRIPTIONS_TABLE_NAME="subscriptions"
export ALLOWED_ORIGINS="http://localhost:5500,http://127.0.0.1:5500"
export PORT="5000"

AWS credentials should be configured through the AWS CLI, IAM role, or environment variables. Do not hardcode AWS credentials in the source code.

5. Run the Flask Backend
python app_backend.py

The backend should start at:

http://localhost:5000
6. Open the Frontend

Open index.html, login.html, register.html, or main.html in a browser.

For local development, a simple local server can be used:

python -m http.server 5500

Then open:

http://localhost:5500
DynamoDB Table Design

This project expects three DynamoDB tables.

Login Table

Table name:

login

Primary key:

email

Example item:

{
  "email": "demo@example.com",
  "user_name": "Demo User",
  "password_hash": "hashed-password-value"
}
Music Table

Table name:

music

Expected fields:

title
artist
album
year
image_url

The backend can use an optional Global Secondary Index:

album-year-index
Subscriptions Table

Table name:

subscriptions

Primary key:

email

Sort key:

song_id

Example item:

{
  "email": "demo@example.com",
  "song_id": "Taylor Swift#Love Story#Fearless#2008",
  "title": "Love Story",
  "artist": "Taylor Swift",
  "album": "Fearless",
  "year": "2008",
  "image_url": "example-image-url"
}
Security Improvements in This Portfolio Version

The original project was cleaned before public release.

Improvements include:

Removed academic report and worklog files
Removed student ID references from public files
Removed hardcoded AWS API Gateway endpoint
Removed hardcoded EC2 IP address
Removed hardcoded load balancer URL
Removed serverless file that required additional rewriting
Replaced plain-text password logic with password hashing
Added environment-based configuration
Added .gitignore rules for private and generated files
Results and Demonstrated Skills

This project demonstrates:

Building REST APIs using Flask
Connecting Python applications to AWS DynamoDB
Handling JSON data between frontend and backend
Implementing user registration and login
Applying password hashing for safer authentication
Designing CRUD-style subscription functionality
Using Git and GitHub for version control
Preparing an academic project for a professional public portfolio
Screenshots and Demo

Screenshots and demo images can be added later in a docs/screenshots/ folder.

Suggested screenshots:

Home page
Register page
Login page
Music search page
Subscription list
DynamoDB table sample with private data hidden
API test result from Postman
What I Learned

Through this project, I practised:

Designing a simple full-stack cloud application
Building Flask API routes
Working with AWS DynamoDB tables and queries
Handling frontend-to-backend communication
Improving security by removing hardcoded credentials and endpoints
Preparing university project work into a portfolio-safe public version
Using GitHub professionally for job applications
Future Improvements

Possible future improvements include:

Move frontend files into a dedicated frontend/ folder
Move backend files into a dedicated backend/ folder
Add Docker support
Add automated backend tests with pytest
Add GitHub Actions for CI checks
Add a sample local JSON database mode for users without AWS access
Add deployed demo screenshots
Add improved frontend styling
Add JWT-based authentication
Add pagination for music search results
Academic Integrity Note

This repository is a portfolio-safe version of an academic project.

It does not include:

Assignment briefs
Rubrics
Protected starter code
Hidden tests
Private datasets
Student IDs
University submission files
API keys
Passwords
AWS credentials

The project has been cleaned and rewritten where needed for public GitHub presentation. It is presented as a learning and portfolio project, not as a complete university solution for reuse by other students.

Author

Janani Byaravalli Pramod Patel
Melbourne, Australia
Master of Artificial Intelligence, RMIT University
Expected completion: December 2026

Licence

This project is shared for portfolio and learning purposes. Add a licence file before reuse or modification.