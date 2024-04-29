document.addEventListener('DOMContentLoaded', function() {
    fetchDataFromCSV();
});

function fetchDataFromCSV() {
    fetch('rfid_button_data.csv')
    .then(response => response.text())
    .then(data => {
        const rows = data.split('\n');
        const issueContainer = document.getElementById('issueContainer');

        rows.forEach(row => {
            const columns = row.split(',');
            const event = columns[1].trim(); // Remove leading and trailing spaces
            const reporterText = columns[3].trim(); // Remove leading and trailing spaces

            // Skip "Access granted" events
            if (event === 'Access granted') {
                return;
            }

            // Create issue card element
            const issueCard = document.createElement('div');
            issueCard.classList.add('col-md-6');
            issueCard.innerHTML = `
                <div class="issue-card card text-center">
                    <div class="card-body">
                        <h5 class="card-title">${event}</h5>
                        <p class="card-text">Status: <button class="btn btn-danger status-btn"><span class="status-text">Reported</span></button></p>
                        <p class="card-text">Last Reported By: ${reporterText}</p>
                        <button type="button" class="btn btn-primary resolve-btn">Solve</button>
                    </div>
                </div>
            `;

            // Add click event listener to resolve button
            const resolveBtn = issueCard.querySelector('.resolve-btn');
            resolveBtn.addEventListener('click', function(event) {
                event.stopPropagation(); // Prevent card click event from triggering
                // Change status to "Resolved"
                const statusElement = issueCard.querySelector('.status-text');
                statusElement.textContent = 'Resolved';
                // Toggle between btn-danger and btn-success classes
                const statusButton = issueCard.querySelector('.status-btn');
                statusButton.classList.toggle('btn-success');
                statusButton.classList.toggle('btn-danger');
            });

            // Add click event listener to issue card
            issueCard.addEventListener('click', function() {
                // Optionally add functionality here when clicking on the card itself
            });

            // Append issue card to the container
            issueContainer.appendChild(issueCard);
        });
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}
