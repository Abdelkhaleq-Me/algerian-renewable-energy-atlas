# Algerian Renewable Energy Atlas

## 1. Project Purpose

The Algerian Renewable Energy Atlas is a digital platform designed to map, quantify, and visualize Algeria's renewable energy potential, specifically focusing on solar, wind, and green hydrogen resources. The platform aims to provide a comprehensive, accessible, and interactive resource for stakeholders interested in exploring and developing renewable energy projects in Algeria. It serves as a decision-support tool by consolidating geospatial data, scientific measurements, and (eventually) AI-powered predictions.

## 2. Project Objectives

* **Map Renewable Energy Resources:** To create a detailed, interactive map of Algeria showing the spatial distribution of solar irradiance, wind speed, and green hydrogen production potential.
* **Provide Quantitative Data:** To offer precise, quantitative data on renewable energy resources at different locations and time scales.
* **Enable Data Analysis:** To equip users with tools to query, analyze, and visualize the data.
* **Facilitate Data Access:** To allow users to download datasets and generate reports.
* **Incorporate AI Predictions:** (Future Goal) To integrate AI-powered models for future predictions.
* **Promote Development:** To support informed decision-making and encourage investment.
* **Be Accessible:** To design a user-friendly platform for all expertise levels.
* **Create an MVP:** Deliver a basic version with all main features.

## 3. Target Audience

* **Energy Developers and Investors:** Companies and individuals seeking renewable energy project sites
* **Government Agencies:** Policymakers and planners
* **Researchers and Academics:** Energy resource researchers
* **NGOs:** Climate change and sustainable development organizations
* **General Public:** Those interested in Algeria's renewable energy potential

## 4. Requirements

### A. Functional Requirements

#### FR1. Interactive Map
* Display interactive Algeria map using Leaflet.js
* Enable zoom, pan, and region selection

#### FR2. Layer Control
* Solar Irradiance (GHI, DNI, DHI)
* Wind Speed
* Green Hydrogen Potential
* Infrastructure
* Administrative Boundaries
* Basemap Options

#### FR3. Filtering
* Energy Type (Solar, Wind, Green Hydrogen)
* Time Period (Daily, Monthly, Annual, Custom Range)
* Prediction Scenario (Baseline, RCP 2.6, RCP 4.5, RCP 8.5) - For future AI integration

#### FR4. Data Query
* Click on the map to retrieve data values at a specific point.
* Select a predefined region (wilaya) from a dropdown or by clicking on the map.
* Draw a custom area on the map to retrieve aggregated data.

#### FR5. Dashboard
* Wilaya Overview: Selected region name and key statistics.
* Time-Series Chart: Plot of renewable energy data over time.
* Comparative Chart: Comparison of potential across regions or energy types.
* Data Table: Display of the raw data used in the charts.

#### FR6. Data Download
* Allow users to download datasets in various formats (CSV, GeoJSON, Shapefile) based on selected filters.

#### FR7. Report Generation (Future Goal)
* Enable users to generate PDF reports summarizing data for a selected region.

#### FR8. AI Prediction (Future Goal)
* Display AI-powered predictions of future renewable energy potential on the map and in the dashboard.

#### FR9. Search (Future Goal)
* Allow users to search for regions or locations by name or coordinates.

#### FR10. Multilingual Support
* Provide the user interface in Arabic, French, and English.

#### FR11. About Page
* Include information about the project, data sources, methodology, and contact details.

### B. Non-Functional Requirements

#### NFR1. Performance
* Map loading time should be under 3 seconds.
* Data retrieval for a selected region should be under 5 seconds.
* Chart rendering should be under 2 seconds.

#### NFR2. Usability
* The user interface should be intuitive and easy to navigate.
* The map controls should be user-friendly.
* The data visualizations should be clear and understandable.

#### NFR3. Accessibility
* The website should be accessible to users with disabilities, complying with WCAG 2.1 Level AA guidelines.
* Provide keyboard navigation.
* Use ARIA attributes for assistive technologies.
* Offer a high-contrast mode.

#### NFR4. Security
* Protect against common web vulnerabilities (SQL injection, XSS).
* Use HTTPS for all communication.

#### NFR5. Scalability
* The system should be designed to handle increasing amounts of data and user traffic.

#### NFR6. Maintainability
* The codebase should be well-organized, documented, and easy to maintain.

#### NFR7. Reliability
* The system should be reliable and available, with minimal downtime.

#### NFR8. Portability
* The system should be able to be deployed on different platforms (e.g., different cloud providers).

#### NFR9. Responsiveness
* The website should adapt to different screen sizes.

## 5. Technology Stack

### Backend
* **Framework:** Flask
* **Extensions:** Flask-RESTful, Flask-SQLAlchemy, Flask-Babel, Flask-Caching, Flask-Migrate
* **Spatial Support:** GeoAlchemy2 with PostgreSQL/PostGIS
* **External Data:** Integration Requests

### Frontend
* **Core:** HTML, CSS, Vanilla JavaScript
* **Mapping:** Leaflet.js
* **Visualization:** Plotly.js/D3.js, Deck.gl

### AI/ML
* **Libraries:** Scikit-learn, TensorFlow

## 6. Website Map and Page Structure

```
Algerian Renewable Energy Atlas (Root)
│
├── Global Header (Persistent Across Pages)
│   ├── Logo
│   ├── Navigation Links
│   │     ├── Home
│   │     ├── Atlas
│   │     ├── Download
│   │     └── About
│   ├── Search Bar 
│   │     └── (Primarily active on the Atlas page for region/coordinate lookup)
│   ├── Language Switch Dropdown (Arabic, French, English)
│   └── Theme Switch Button (Light/Dark)
│
├── Home Page
│   ├── Hero Section
│   │     ├── Headline & Sub-headline (Introduce the Atlas)
│   │     ├── Algeria Map Overview 
│   │     │      └── (Static image or simplified interactive map)
│   │     └── Call-to-Action Buttons
│   │            ├── "Explore the Atlas Map" → Atlas Page
│   │            └── "Download Data & Reports" → Download Page
│   │
│   ├── Key Statistics Section
│   │     └── Infographics/Counters (Solar, Wind, Green Hydrogen)
│   │
│   ├── "Why Renewable Energy in Algeria?" Section
│   │     └── (Benefits, icons, and brief descriptions)
│   │
│   └── "About the Atlas" Section
│         └── (Brief overview with a link to the About Page)
│
├── Atlas Page (Interactive Exploration)
│   ├── Split-Screen Layout
│   │
│   ├── Left Panel: Interactive Map
│   │     ├── Map Container
│   │     │      └── (Leaflet.js integration with OpenStreetMap tiles)
│   │     ├── Layer Control
│   │     │      └── (Toggle Solar, Wind, Green Hydrogen layers)
│   │     ├── Filter Controls
│   │     │      ├── Energy Type Dropdown
│   │     │      └── Search Functionality (Keyword, Region Name, Coordinates)
│   │     ├── Map Interactivity
│   │     │      └── (Zoom, pan, mouseover tooltips with ARIA labels)
│   │     ├── Legend (Clear color scale explanations)
│   │     └── Loading Indicator (Highly visible during data fetches)
│   │
│   ├── Right Panel: Dashboard & Data Visualization
│   │     ├── Welaya Overview
│   │     │      ├── Region Selector (Dropdown or interactive list synced with map)
│   │     │      └── Stats Cards (Aggregated renewable energy metrics)
│   │     ├── Time-Series Chart
│   │     │      └── (Plotly.js/D3.js with built-in zoom/pan controls)
│   │     ├── Comparative Analytics Chart
│   │     │      └── (Bar chart comparing regions/energy types)
│   │     ├── Data Table (Optional raw data display)
│   │     └── "Download Visualization" Button (Export as PNG/PDF)
│   │
│   ├── Accessibility Enhancements
│   │     ├── Keyboard Navigability
│   │     ├── ARIA Labels on interactive elements
│   │     └── High-Contrast Mode options
│   │
│   └── Mobile Optimization
│         └── (Responsive design ensuring split-screen adapts for tablets/smartphones)
│
├── Download Page
│   ├── Download Datasets Section
│   │     ├── Filters (Energy Type, Welaya)
│   │     ├── Dataset Format Dropdown (CSV, GeoJSON)
│   │     └── "Download Dataset" Button (Backend handles generation)
│   │
│   ├── Generate Report Section
│   │     ├── Report Filters (Similar to dataset filters)
│   │     ├── "Generate Report" Button (PDF generation)
│   │     └── "Download Report" Link (Displayed after generation)
│   │
│   └── Information & Instructions
│         └── (Guidance on how to use download features)
│
├── About Page
│   ├── About the Project Section
│   │     └── (Detailed background and objectives)
│   ├── Renewable Energy in Algeria Context Section
│   │     └── (Educational content on benefits and potential)
│   ├── Data and Methodology Section
│   │     └── (Sources and technical overview of methods & AI predictions)
│   ├── Technical FAQs Section
│   │     └── (Common questions answered)
│   ├── Contact Us Section
│   │     └── (Basic contact information)
│   └── Credits and Acknowledgements Section
│         └── (Data providers, partners, contributors)
│
├── Global Footer (Persistent Across Pages, except Atlas if full-screen map is preferred)
│   ├── Legal Information
│   ├── Contact Details
│   ├── Quick Links (Privacy Policy, Terms of Use)
│   └── Social Media Links
│
└── Cross-Cutting Technical & Performance Considerations
      ├── Visible & Informative Loading Indicators (Across data-intensive operations)
      ├── Caching Strategies (To optimize data fetching and enhance responsiveness)
      └── Optimized Data Handling (Ensuring smooth performance on all devices)

```

## 7. Project Structure

```
algerian-renewable-energy-atlas/
├── app/
│   ├── __init__.py          # Initialize Flask app and load extensions
│   ├── config.py            # Configuration settings for different environments
│   ├── extensions.py        # Initialize Flask extensions (SQLAlchemy, Babel, Caching, etc.)
│   ├── models/              # Database models and spatial models using SQLAlchemy/GeoAlchemy2
│   │   ├── __init__.py
│   │   └── energy_models.py
│   ├── routes/              # Flask routes for different pages
│   │   ├── __init__.py
│   │   ├── home.py          # Routes for the Home page
│   │   ├── atlas.py         # Routes for the Atlas page (interactive map)
│   │   ├── download.py      # Routes for the Download page
│   │   └── about.py         # Routes for the About page
│   ├── api/                 # RESTful API endpoints using Flask-RESTful
│   │   ├── __init__.py
│   │   └── endpoints.py
│   ├── ai/                  # AI/ML modules for energy potential prediction
│   │   ├── __init__.py
│   │   ├── models.py        # ML model definitions (Scikit-learn/TensorFlow)
│   │   └── predict.py       # Prediction routines exposed to the Flask app
│   ├── utils/               # Utility functions, helpers, and data processing scripts (e.g., with GeoPandas)
│   │   ├── __init__.py
│   │   └── geospatial.py
│   ├── templates/           # HTML templates (Jinja2)
│   │   ├── base.html        # Base template with global header/footer
│   │   ├── home.html
│   │   ├── atlas.html
│   │   ├── download.html
│   │   └── about.html
│   └── static/              # Frontend assets
│       ├── css/             # Custom CSS files
│       ├── js/              # Vanilla JS files and library integrations (Leaflet.js, Plotly.js/D3.js, Deck.gl)
│       └── images/          # Image assets (logos, maps, icons)
│
├── migrations/              # Database migration scripts (managed by Flask-Migrate)
├── tests/                   # Unit and integration tests
│   ├── __init__.py
│   ├── test_routes.py
│   ├── test_api.py
│   └── test_models.py
├── requirements.txt         # Python dependencies list
├── run.py                   # Application entry point to run the Flask app
└── README.md                # Project overview and documentation
```