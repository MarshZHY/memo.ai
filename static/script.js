document.addEventListener("DOMContentLoaded", () => {
    const currentDate = document.getElementById("entry-date").value;
    fetchEntry(currentDate);  // Load current date's data on page load
    fetchData();              // Load all data points for the graph
    document.getElementById("entry-date").addEventListener("change", handleDateChange);
});

function submitEntry() {
    const diaryText = document.getElementById("diary-text").value;
    const entryDate = document.getElementById("entry-date").value;
    
    if (diaryText.trim() === "") {
        alert("Please enter your diary entry.");
        return;
    }

    fetch('/submit_entry', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: new URLSearchParams({diary: diaryText, date: entryDate})
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("stress-feedback").textContent = `Feedback: ${data.feedback} (Stress Level: ${data.stress_level})`;
        document.getElementById("streak").textContent = `🔥 ${data.streak}`; // Update streak display
        fetchData();  // Refresh chart with new entry
        document.getElementById("diary-text").value = "";
    })
    .catch(error => console.error("Error submitting entry:", error));
}

function clearEntry() {
    const entryDate = document.getElementById("entry-date").value;
    fetch(`/clear_entry/${entryDate}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            fetchData();  // Refresh the chart after clearing
            document.getElementById("diary-text").value = "";
            document.getElementById("stress-feedback").textContent = "Feedback will appear here after submitting.";
        })
        .catch(error => console.error("Error clearing entry:", error));
}

function fetchData() {
    fetch('/get_data')
        .then(response => response.json())
        .then(entries => {
            const dates = entries.map(entry => entry.date);
            const stressLevels = entries.map(entry => entry.stress_level);
            const selectedDate = document.getElementById("entry-date").value;
            renderPlotlyChart(dates, stressLevels, selectedDate);
        })
        .catch(error => console.error("Error fetching data:", error));
}

function renderPlotlyChart(dates, stressLevels, selectedDate) {
    const data = [{
        x: dates,
        y: stressLevels,
        mode: 'lines+markers',
        type: 'scatter',
        marker: {
            size: 6,
            color: dates.map(date => date === selectedDate ? '#ff9500' : '#007aff'), // Highlight selected date in orange
            symbol: dates.map(date => date === selectedDate ? 'star' : 'circle')    // Use star symbol for selected date
        },
        line: { color: '#007aff' }
    }];

    const layout = {
        title: 'Stress Level Over Time',
        xaxis: {
            title: 'Date',
            tickmode: 'array',
            tickvals: dates,
            ticktext: dates
        },
        yaxis: {
            title: 'Stress Level',
            range: [0, 100],
            fixedrange: true
        },
        margin: { t: 30 },
        scrollZoom: true,
        dragmode: 'pan',
        modebar: { orientation: "h" }
    };

    Plotly.newPlot('stressChart', data, layout, { responsive: true });

    // Set up click event to fetch entry and update the date picker
    document.getElementById('stressChart').on('plotly_click', function(eventData) {
        const date = eventData.points[0].x;
        fetchEntry(date);
        document.getElementById("entry-date").value = date; // Update date picker
        fetchData(); // Re-render the graph with the new selected date
    });
    
    // Add a double-click event for resetting the zoom
    document.getElementById('stressChart').on('plotly_doubleclick', function() {
        Plotly.relayout('stressChart', {
            'xaxis.autorange': true,
            'yaxis.autorange': true
        });
    });
}

function fetchEntry(date) {
    fetch(`/get_entry/${date}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                document.getElementById("diary-text").value = "";
                document.getElementById("stress-feedback").textContent = "No data available for this date.";
            } else {
                document.getElementById("stress-feedback").textContent = `Feedback: ${data.feedback} (Stress Level: ${data.stress_level})`;
                document.getElementById("diary-text").value = data.text;
            }
        })
        .catch(error => console.error("Error fetching entry:", error));
}

// Handle date picker changes to load entry for the selected date
function handleDateChange() {
    const selectedDate = document.getElementById("entry-date").value;
    fetchEntry(selectedDate);
    fetchData(); // Update graph highlight to reflect the selected date
}
