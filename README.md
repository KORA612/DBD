Data Visualization Web Application

This is a web application built with Flask for visualizing datasets uploaded by users. Users can upload CSV files, select features, and choose from various plot types to visualize their data.

Features
User Authentication: Users can register, log in, and log out securely.
Dataset Management: Users can upload CSV datasets, which are stored securely.
Visualization: Users can select datasets, choose x and y features, and select plot types for visualization.
Interactive Plots: Various plot types are supported, including scatter plots, line plots, histograms, box plots, and pair plots.
Prerequisites
Python 3.6+
Flask
Pandas
Matplotlib
Seaborn
Bootstrap (for front-end styling)

Usage
Register: Create a new account to access the dashboard.
Log in: Log in with your credentials.
Upload Dataset: Navigate to the upload page to upload CSV datasets.
Visualize Data: Navigate to the visualize page to select a dataset, x and y features, and plot type for visualization.
Log out: Log out from your account.
Project Structure

Copy code
├── app.py                    # Main application file
├── config.py                 # Configuration file
├── forms.py                  # Flask-WTF forms
├── models.py                 # SQLAlchemy models (User, Dataset)
├── static/                   # Static assets (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── img/
├── templates/                # HTML templates
│   ├── dashboard.html
│   ├── home.html
│   ├── layout.html
│   ├── login.html
│   ├── register.html
│   ├── upload.html
│   └── visualize.html
├── visualize.py              # Data visualization functions
└── requirements.txt          # Python dependencies
Contributing
Contributions are welcome! Please fork the repository and create a pull request with your improvements.

License
This project is licensed under the MIT License - see the LICENSE file for details.
