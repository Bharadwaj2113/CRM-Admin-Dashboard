# CRM-Admin-Dashboard

**CRM-Admin-Dashboard** is a web application designed to help businesses manage their customer relationships efficiently. It provides a centralized platform for admins to track customer details, record interactions, generate personalized recommendations, send emails, and analyze customer engagement.

## Features

- **User Authentication**: Secure login system for admins.
- **Customer Management**: Add, view, and search for customers, including their purchase history.
- **Interactions Tracking**: Record and review customer engagements (e.g., calls, emails).
- **Personalized Recommendations**: AI-powered product suggestions based on purchase history.
- **Email Integration**: Send targeted emails like coupons directly from the app.
- **Analytics Dashboard**: Visualize customer interaction data with charts.

## Technologies Used

- **Frontend**: React, Chart.js
- **Backend**: Flask, PostgreSQL
- **AI Integration**: Google Gemini API for recommendations
- **Email Service**: SendGrid for sending emails
- **Authentication**: JWT (JSON Web Tokens)

## Setup Instructions

### Prerequisites

- **Node.js** and **npm** (for the frontend)
- **Python 3.x** and **pip** (for the backend)
- **PostgreSQL** (for the database)
- **Git** (for cloning the repository)

###.env
DB_NAME=crmconnect
DB_USER=your_postgres_user
DB_PASS=your_postgres_password
DB_HOST=localhost
GOOGLE_API_KEY=your_google_api_key
SECRET_KEY=your_secret_key
EMAIL_SENDER=your_email@example.com
EMAIL_PASSWORD=your_email_password

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/CRM-Admin-Dashboard.git
   cd CRM-Admin-Dashboard



