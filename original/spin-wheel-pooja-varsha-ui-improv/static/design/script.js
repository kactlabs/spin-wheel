document.addEventListener('DOMContentLoaded', () => {
    const setupScreen = document.getElementById('setupScreen');
    const appScreen = document.getElementById('appScreen');
    const startButton = document.getElementById('startButton');
    const participantsTextarea = document.getElementById('participants');
    const numTeamsInput = document.getElementById('numTeams');
    const numTeamsGroup = document.getElementById('numTeamsGroup');
    const setupError = document.getElementById('setupError');
    const teamGeneratorRadio = document.getElementById('teamGenerator');
    const simplePickerRadio = document.getElementById('simplePicker');

    const wheel = document.getElementById('wheel');
    const spinButton = document.getElementById('spinButton');
    const resetButton = document.getElementById('resetButton');
    const teamsContainer = document.getElementById('teamsContainer');
    const pickedNamesList = document.getElementById('pickedNamesList');
    const appTitle = document.getElementById('appTitle');

    const resultModal = document.getElementById('resultModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalSubtitle = document.getElementById('modalSubtitle');
    const modalCloseButton = document.getElementById('modalCloseButton');

    let participants = [];
    let numTeams = 0;
    let gameMode = 'teams'; // 'teams' or 'simple'
    let availableParticipants = [];
    let currentTeams = {};

    // Event Listeners for Setup Screen
    teamGeneratorRadio.addEventListener('change', () => {
        gameMode = 'teams';
        numTeamsGroup.style.display = 'block';
    });

    simplePickerRadio.addEventListener('change', () => {
        gameMode = 'simple';
        numTeamsGroup.style.display = 'none';
    });

    startButton.addEventListener('click', () => {
        const namesInput = participantsTextarea.value.trim();
        if (!namesInput) {
            setupError.textContent = 'Please enter participant names.';
            return;
        }
        participants = namesInput.split('\n').map(name => name.trim()).filter(name => name !== '');
        if (participants.length === 0) {
            setupError.textContent = 'Please enter valid participant names.';
            return;
        }

        if (gameMode === 'teams') {
            numTeams = parseInt(numTeamsInput.value, 10);
            if (isNaN(numTeams) || numTeams < 1) {
                setupError.textContent = 'Please enter a valid number of teams.';
                return;
            }
            if (numTeams > participants.length) {
                setupError.textContent = 'Number of teams cannot exceed the number of participants.';
                return;
            }
            appTitle.textContent = 'Spin to Assign!';
        } else {
            numTeams = 1; // Not used for simple picker, but set for consistency
            appTitle.textContent = 'Spin to Pick!';
        }
        
        setupError.textContent = '';
        initializeWheelAndTeams();
        setupScreen.style.display = 'none';
        appScreen.style.display = 'grid';
    });

    resetButton.addEventListener('click', () => {
        appScreen.style.display = 'none';
        setupScreen.style.display = 'flex';
        wheel.innerHTML = ''; // Clear wheel segments
        teamsContainer.innerHTML = ''; // Clear teams
        pickedNamesList.innerHTML = ''; // Clear picked names
        participantsTextarea.value = ''; // Clear textarea
        numTeamsInput.value = '2'; // Reset num teams
        teamGeneratorRadio.checked = true; // Reset mode
        numTeamsGroup.style.display = 'block';
    });

    spinButton.addEventListener('click', spinWheel);
    modalCloseButton.addEventListener('click', closeModal);

    function initializeWheelAndTeams() {
        wheel.innerHTML = '';
        teamsContainer.innerHTML = '';
        pickedNamesList.innerHTML = '';
        availableParticipants = [...participants]; // Copy all participants to available list

        // Create wheel segments
        const arc = d3.arc().outerRadius(150).innerRadius(0);
        const pie = d3.pie().sort(null).value(1); // Each participant gets equal slice

        const svg = d3.select(wheel).append("svg")
            .attr("width", 300)
            .attr("height", 300)
            .append("g")
            .attr("transform", "translate(150,150)");

        const g = svg.selectAll(".arc")
            .data(pie(availableParticipants))
            .enter().append("g")
            .attr("class", "arc");

        g.append("path")
            .attr("d", arc)
            .style("fill", (d, i) => d3.schemeCategory10[i % 10]); // Use D3's color scheme

        g.append("text")
            .attr("transform", d => `translate(${arc.centroid(d)}) rotate(${getTextRotation(d)})`)
            .attr("text-anchor", "middle")
            .text(d => d.data)
            .style("fill", "#fff")
            .style("font-size", "12px");

        // Initialize teams if in team generator mode
        if (gameMode === 'teams') {
            currentTeams = {};
            for (let i = 1; i <= numTeams; i++) {
                currentTeams[`Team ${i}`] = [];
                const teamCard = document.createElement('div');
                teamCard.className = 'team-card';
                teamCard.innerHTML = `<h3>Team ${i}</h3><ul id="team${i}List"></ul>`;
                teamsContainer.appendChild(teamCard);
            }
        }
    }

    function getTextRotation(d) {
        const angle = (d.startAngle + d.endAngle) / 2 * 180 / Math.PI;
        return (angle > 90 && angle < 270) ? angle + 180 : angle;
    }

    function spinWheel() {
        if (availableParticipants.length === 0) {
            showModal('No Participants Left!', 'Please reset the wheel to add more names.');
            return;
        }

        spinButton.disabled = true;
        const randomIndex = Math.floor(Math.random() * availableParticipants.length);
        const selectedName = availableParticipants[randomIndex];

        // Calculate rotation for D3 wheel
        const totalRotation = 360 * 5 + (360 - (randomIndex * degreePerItem + degreePerItem / 2)); // Spin 5 full rotations + land on target
        
        d3.select(wheel)
            .transition()
            .duration(5000)
            .attrTween("transform", () => {
                const interpolate = d3.interpolate(0, totalRotation);
                return t => `rotate(${interpolate(t)})`;
            })
            .end()
            .then(() => {
                handleSpinResult(selectedName, randomIndex);
            });
    }

    function handleSpinResult(selectedName, originalIndex) {
        confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 }
        });

        if (gameMode === 'teams') {
            const teamIndex = Object.values(currentTeams).findIndex(team => team.length < Math.ceil(participants.length / numTeams));
            if (teamIndex !== -1) {
                const teamName = `Team ${teamIndex + 1}`;
                currentTeams[teamName].push(selectedName);
                const teamList = document.getElementById(`team${teamIndex + 1}List`);
                const listItem = document.createElement('li');
                listItem.textContent = selectedName;
                teamList.appendChild(listItem);
                showModal('Winner!', `${selectedName} joins ${teamName}!`);
            } else {
                showModal('All Teams Full!', `${selectedName} was picked but teams are full.`);
            }
        } else { // Simple Picker Mode
            const listItem = document.createElement('li');
            listItem.textContent = selectedName;
            pickedNamesList.appendChild(listItem);
            showModal('Winner!', `${selectedName} has been picked!`);
        }

        // Remove selected participant from available list and re-render wheel
        availableParticipants.splice(originalIndex, 1);
        updateWheel();
        spinButton.disabled = false;

        if (availableParticipants.length === 0 && gameMode === 'simple') {
            showModal('All Names Picked!', 'The wheel is empty. Reset to play again.');
            spinButton.disabled = true;
        } else if (availableParticipants.length === 0 && gameMode === 'teams') {
            showModal('All Participants Assigned!', 'All participants have been assigned to teams. Reset to play again.');
            spinButton.disabled = true;
        }
    }

    function updateWheel() {
        wheel.innerHTML = ''; // Clear existing SVG
        const arc = d3.arc().outerRadius(150).innerRadius(0);
        const pie = d3.pie().sort(null).value(1);

        const svg = d3.select(wheel).append("svg")
            .attr("width", 300)
            .attr("height", 300)
            .append("g")
            .attr("transform", "translate(150,150)");

        const g = svg.selectAll(".arc")
            .data(pie(availableParticipants))
            .enter().append("g")
            .attr("class", "arc");

        g.append("path")
            .attr("d", arc)
            .style("fill", (d, i) => d3.schemeCategory10[i % 10]);

        g.append("text")
            .attr("transform", d => `translate(${arc.centroid(d)}) rotate(${getTextRotation(d)})`)
            .attr("text-anchor", "middle")
            .text(d => d.data)
            .style("fill", "#fff")
            .style("font-size", "12px");
    }

    function showModal(title, subtitle) {
        modalTitle.textContent = title;
        modalSubtitle.textContent = subtitle;
        resultModal.style.display = 'flex';
    }

    function closeModal() {
        resultModal.style.display = 'none';
    }
});
