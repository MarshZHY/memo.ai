
Watch a quick video demo of MeMoDot AI [here](https://youtu.be/7y9JksBULZs) or use the embedded player below:

[![MeMoDot AI Video Demo](https://img.youtube.com/vi/7y9JksBULZs/0.jpg)](https://youtu.be/7y9JksBULZs)

<iframe width="560" height="315" src="https://www.youtube.com/embed/7y9JksBULZs" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


# MeMoDot AI ( Host on Vercel mai dai TOT )

This project provides a Flask-based web application, **MeMoDot AI**, designed to help users track their daily moods and stress levels over time. Users can input diary entries, receive AI-generated feedback on their stress levels, and visualize their mood progression via an interactive chart. This application integrates various components, including a database to store entries, an AI model to analyze stress levels, and a front-end for user interaction.

## Project Structure

- **Flask Back-End**: Handles routing, API integration for stress analysis, and database management.
- **Database (SQLite)**: Stores diary entries with date, text, stress level, and AI feedback.
- **OpenAI Typhoon API**: Utilized for stress level analysis and feedback generation.
- **Front-End (HTML/CSS/JavaScript)**: Provides an interface for inputting entries, viewing feedback, and interacting with the stress chart.

## Code Walkthrough

### 1. Configuration and Database Setup

- **Database Configuration**: The SQLite database (`data.db`) is used to store diary entries.
- **Typhoon API Key**: A placeholder for the `TYPHOON_API_KEY` is provided for integration with OpenAI Typhoon's stress analysis.
- **Database Initialization**:
  - `init_db()`: Creates the `diary_entries` table with fields for date, input text, stress level, and AI feedback if it doesn't exist.

### 2. Utility Functions

- **Database Connection (`get_db`)**: Connects to the SQLite database and attaches it to the Flask application context.
- **Calculate Streak (`calculate_streak`)**: Determines the user's streak of consecutive days with diary entries, counting the number of consecutive days with entries in reverse chronological order.

### 3. Stress Analysis Function (`analyze_stress`)

This function:
- Connects to the Typhoon API to analyze diary entries.
- The Typhoon API is instructed to gauge stress levels from diary text using examples.
- The function parses the AI response to extract the stress level and feedback.

### 4. Flask Routes

- **Index (`/`)**: Renders the main HTML template with the current date and streak information.
- **Submit Entry (`/submit_entry`)**:
  - Retrieves the diary entry and date from the POST request.
  - Calls `analyze_stress` to evaluate stress.
  - Stores the entry in the database.
  - Updates and returns the user's streak, stress level, and AI feedback.
- **Get All Data (`/get_data`)**: Fetches all entries (dates and stress levels) for visualizing mood progression.
- **Get Entry by Date (`/get_entry/<date>`)**: Retrieves a specific entry by date, including its stress level and feedback.
- **Clear Entry (`/clear_entry/<date>`)**: Deletes an entry by date, allowing users to remove past entries if needed.

### 5. Front-End (HTML & JavaScript)

The main user interface includes:

- **Date Picker and Entry Section**:
  - Allows users to select a date and input their diary entry.
  - Displays the current streak and AI feedback for each entry.
- **Stress Level Chart**:
  - Uses Plotly.js to render an interactive line chart visualizing stress levels over time.
  - Users can click on specific dates to view detailed feedback or reset the chart to its original state.
- **JavaScript Functions**:
  - `submitEntry()`: Submits the diary entry to the back-end, retrieves stress analysis, updates the chart, and clears the entry field.
  - `clearEntry()`: Removes an entry from the database by date.
  - `fetchData()`: Retrieves all entries from the back-end for chart rendering.
  - `renderPlotlyChart()`: Configures and renders the Plotly line chart with stress levels.
  - `fetchEntry()`: Loads a specific entry based on the selected date, displaying feedback and text content.
  - `handleDateChange()`: Updates the chart and fetches entry details when the date selection changes.

## How to Run the Application

1. **Set up the environment**:
   - Install dependencies: `Flask`, `sqlite3`, `openai`, and any required front-end libraries.
2. **Configure the Typhoon API Key**: Replace `'your_typhoon_api_key'` in the code with a valid Typhoon API key.
3. **Start the Application**:
   ```bash
   python app.py```
4.  Access the Interface: Open a browser and navigate to http://127.0.0.1:5000/ to interact with the app.