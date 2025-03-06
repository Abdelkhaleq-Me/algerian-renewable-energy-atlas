# Algerian Renewable Energy Atlas

## 1. Project Purpose

The Algerian Renewable Energy Atlas is a digital platform designed to map, quantify, and visualize Algeria's renewable energy potential, specifically focusing on solar, wind, and green hydrogen resources. The platform aims to provide a comprehensive, accessible, and interactive resource for stakeholders interested in exploring and developing renewable energy projects in Algeria. It serves as a decision-support tool by consolidating geospatial data, scientific measurements, and (eventually) AI-powered predictions.

## 2. Project Objectives

*   **Map Renewable Energy Resources:** To create a detailed, interactive map of Algeria showing the spatial distribution of solar irradiance, wind speed, and green hydrogen production potential.
*   **Provide Quantitative Data:** To offer precise, quantitative data on renewable energy resources at different locations and time scales.
*   **Enable Data Analysis:** To equip users with tools to query, analyze, and visualize the data.
*   **Facilitate Data Access:** To allow users to download datasets and generate reports.
*   **Incorporate AI Predictions:** (Future Goal) To integrate AI-powered models for future predictions.
*   **Promote Development:** To support informed decision-making and encourage investment.
*   **Be Accessible:** To design a user-friendly platform for all expertise levels.
*   **Create an MVP:** Deliver a basic version with all main features.

## 3. Target Audience

*   **Energy Developers and Investors:** Companies and individuals seeking renewable energy project sites
*   **Government Agencies:** Policymakers and planners
*   **Researchers and Academics:** Energy resource researchers
*   **NGOs:** Climate change and sustainable development organizations
*   **General Public:** Those interested in Algeria's renewable energy potential

## 4. Requirements

### A. Functional Requirements

#### FR1. Interactive Map

*   Display interactive Algeria map using Leaflet.js
*   Enable zoom, pan, and region selection

#### FR2. Layer Control

*   Solar Irradiance (GHI, DNI, DHI)
*   Wind Speed (10, 50, 100)
*   Green Hydrogen Potential
*   Basemap Options

#### FR3. Filtering

*   Energy Type (Solar, Wind, Green Hydrogen)
*   Time Period (Daily, Monthly, Annual, Custom Range)
*   Prediction Scenario (Baseline, RCP 2.6, RCP 4.5, RCP 8.5) - For future AI integration

#### FR4. Data Query

*   Click on the map to retrieve data values at a specific point.  **This will also trigger retrieval of data from the NASA POWER API for display and plotting on the dashboard.**
*   Select a predefined region (wilaya) from a dropdown or by clicking on the map.
*   Draw a custom area on the map to retrieve aggregated data.

#### FR5. Dashboard

*   Wilaya Overview: Selected region name and key statistics.
*   Time-Series Chart: Plot of renewable energy data over time.  **This includes plots from both local data and data fetched from the NASA POWER API.**
*   Comparative Chart: Comparison of potential across regions or energy types.
*   Data Table: Display of the raw data used in the charts.

#### FR6. Data Download

*   Allow users to download datasets in various formats (CSV, GeoJSON, Shapefile) based on selected filters.

#### FR7. Report Generation (Future Goal)

*   Enable users to generate PDF reports summarizing data for a selected region.

#### FR8. AI Prediction (Future Goal)

*   Display AI-powered predictions of future renewable energy potential on the map and in the dashboard.

#### FR9. Search (Future Goal)

*   Allow users to search for regions or locations by name or coordinates.

#### FR10. Multilingual Support

*   Provide the user interface in Arabic, French, and English.

#### FR11. About Page

*   Include information about the project, data sources, methodology, and contact details.

### B. Non-Functional Requirements

#### NFR1. Performance

*   Map loading time should be under 3 seconds.
*   Data retrieval for a selected region should be under 5 seconds.  **This includes data retrieval from the NASA POWER API.**
*   Chart rendering should be under 2 seconds.

#### NFR2. Usability

*   The user interface should be intuitive and easy to navigate.
*   The map controls should be user-friendly.
*   The data visualizations should be clear and understandable.

#### NFR3. Accessibility

*   The website should be accessible to users with disabilities, complying with WCAG 2.1 Level AA guidelines.
*   Provide keyboard navigation.
*   Use ARIA attributes for assistive technologies.
*   Offer a high-contrast mode.

#### NFR4. Security

*   Protect against common web vulnerabilities (SQL injection, XSS).
*   Use HTTPS for all communication.

#### NFR5. Scalability

*   The system should be designed to handle increasing amounts of data and user traffic.

#### NFR6. Maintainability

*   The codebase should be well-organized, documented, and easy to maintain.

#### NFR7. Reliability

*   The system should be reliable and available, with minimal downtime.

#### NFR8. Portability

*   The system should be able to be deployed on different platforms (e.g., different cloud providers).

#### NFR9. Responsiveness

*   The website should adapt to different screen sizes.

## 5. Technology Stack

### Backend

*   **Framework:** Flask
*   **Extensions:** Flask-RESTful, Flask-SQLAlchemy, Flask-Babel, Flask-Caching, Flask-Migrate
*   **Spatial Support:** GeoAlchemy2 with PostgreSQL/PostGIS
*   **External Data:** Integration Requests (specifically, using the `requests` library to interact with the NASA POWER API)

### Frontend

*   **Core:** HTML, Tailwind CSS, Vanilla JavaScript
*   **Mapping:** Leaflet.js
*   **Visualization:** Plotly.js/D3.js, Deck.gl

### AI/ML

*   **Libraries:** Scikit-learn, TensorFlow

## Files to load on database:

*   **Administrative boundaries (Geojson):** algeria_boundry.json, algeria_welayes.json
*   **Solar raster (GeoTiff):** GHI.tif, DNI.tif, PVOUT.tif, TEMP.tif
*   **Wind raster (GeoTiff):** DZA_wind-speed_10m.tif, DZA_wind-speed_50m.tif, DZA_wind-speed_100m.tif, DZA_wind-speed_150m.tif
*   **Green Hydrogen (GeoTiff):** comming soon....

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
│   ├── __init__.py               # Application factory, registers blueprints & extensions
│   ├── config.py                 # Configuration settings (development, production, etc.)
│   ├── extensions.py             # Initialization of extensions (SQLAlchemy, Migrate, Babel, Cache)
│   ├── models/
│   │   ├── __init__.py           # (Optional) Aggregates model imports
│   │   └── energy_models.py      # Your spatial and raster models
│   ├── routes/
│   │   ├── __init__.py           # Initializes and registers blueprints for site pages
│   │   ├── home.py               # Routes for the Home page
│   │   ├── atlas.py              # Routes for the Atlas page (includes map integration)
│   │   ├── download.py           # Routes for the Download page
│   │   └── about.py              # Routes for the About page
│   ├── api/
│   │   ├── __init__.py           # API blueprint initialization (api_bp and Api instance)
│   │   └── endpoints.py          # RESTful endpoints for spatial and external data
│   └── utils/
│       └── load_geojson.py       # Script to load GeoJSON data into the database
├── migrations/                   # Flask-Migrate migration scripts
│   ├── env.py                    # Alembic environment configuration
│   ├── script.py.mako            # Migration script template
│   └── versions/
│       ├── 7babb588c434_initial_migration_create_tables_for_.py
│       └── 952b043a72dc_initial_migration_create_tables_for_.py
├── static/
│   ├── css/
│   │   ├── theme.css             # Contains CSS variables for light/dark themes
│   │   └── styles.css            # Global CSS styles
│   ├── js/
│   │   └── script.js             # Global JavaScript functions and event handlers
│   └── images/
│       ├── logo.png              # Site logo
|       ├── background.jpg                   
│       └── favicon.png           # Favicon for your site
├── templates/
│   ├── base.html                 # Base template with header, footer, and global assets
│   ├── home.html                 # Home page template (extends base.html)
│   ├── atlas.html                # Atlas page template
│   ├── download.html             # Download page template
│   ├── about.html                # About page template
│   └── errors/
│       ├── 400.html
|       ├── 403.html
|       ├── 404.html         # Custom 404 error page
│       └── 500.html              # Custom 500 error page
├── .env                   # Environment file for Flask (e.g., FLASK_APP=run.py FLASK_ENV=development)
├── requirements.txt              # List of Python dependencies
├── README.md                     # Project documentation
└── run.py                        # Entry point to run the Flask application

```

## 8. NASA POWER API Integration Details

This section provides details on how the NASA POWER API is integrated.

**API Endpoints Used:**

*   **Daily Temperature (T2M):**
    `https://power.larc.nasa.gov/api/temporal/daily/point?community=RE&parameters=T2M&latitude=${lat}&longitude=${lon}&start=20240101&end=${currentdate}`

*   **Daily All Sky Surface Shortwave Downward Irradiance (ALLSKY_SFC_SW_DWN):**
    `https://power.larc.nasa.gov/api/temporal/daily/point?community=RE&parameters=ALLSKY_SFC_SW_DWN&latitude=${lat}&longitude=${lon}&start=20240101&end=${currentdate}`

*   **Daily Wind Speed at 10 Meters (WS10M):**
    `https://power.larc.nasa.gov/api/temporal/daily/point?community=RE&parameters=WS10M&latitude=${lat}&longitude=${lon}&start=20240101&end=${currentdate}`

*   **Daily Wind Speed at 50 Meters (WS50M):**
    `https://power.larc.nasa.gov/api/temporal/daily/point?community=RE&parameters=WS50M&latitude=${lat}&longitude=${lon}&start=20240101&end=${currentdate}`

**Where:**

*   `${lat}`:  Latitude of the clicked point on the map.
*   `${lon}`:  Longitude of the clicked point on the map.
*   `${currentdate}`:  The current date in YYYYMMDD format.

