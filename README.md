# VP Bank App
![Fast Money.png](Fast%20Money.png)

## Introduction

Welcome to VP Bank App, a banking application designed to provide users with a seamless and secure banking experience. This README file contains information about the application's technology stack, features, API endpoints, and usage guidelines.

## Tech Stack

### Backend

- **Language**: Python
- **Framework**: Flask
- **Database**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **Email Service**: SMTP for password recovery

### Frontend

- **GUI Library**: Tkinter (Python's standard GUI library)
- **Styling**: Custom styles for a user-friendly interface

## Features

- **User Authentication**: Secure user registration and login.
- **Account Management**: View account balance, transaction history, and perform transactions.
- **Investment Options**: Calculate loan details, perform investment calculations.
- **Statement Generation**: View detailed transaction statements.
- **Password Recovery**: Reset passwords via email.

## API Endpoint

The VP Bank App does not currently expose any external API endpoints.

## Usage

1. **Installation**: Clone the repository and install the required dependencies.
   
```bash
   git clone https://github.com/220296006/vp-bank-app.git
   cd vp-bank-app
   pip install -r requirements.txt
```

2. **Interact with the GUI**
Use the intuitive graphical user interface to explore the features.

## Functional Requirements

1. User Registration and Login
- Users can create accounts with a unique username and email.
- Existing users can log in securely. 

2. Account Management
- View account balance.
- Perform deposits and withdrawals.

3. Investment Options
- Calculate loan details (bond/home loan).
- Perform investment calculations.

4. Statement Generation
-  View detailed transaction statements.

5. Password Recovery
- Reset passwords via email.

## Non-Functional Requirements
1. Security
- Passwords stored securely using encryption.
- JWT tokens for secure authentication.

2. User Experience
- Intuitive and responsive GUI for easy navigation.
- Prompt error messages for user guidance.

- 3. Reliability
- Robust error handling to ensure application stability.

## Conclusion
VP Bank App is designed to provide a reliable and user-friendly banking experience. Your feedback is valuable; feel free to contribute or report issues. Thank you for choosing VP Bank!
