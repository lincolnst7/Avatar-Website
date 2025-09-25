// Game state
let characters = [];
let targetCharacter = null;
let guessCount = 0;
let gameActive = false;

// DOM Elements
const gameSettings = document.getElementById('gameSettings');
const gameArea = document.getElementById('gameArea');
const characterInput = document.getElementById('characterInput');
const autoComplete = document.getElementById('autoComplete');
const guessRows = document.getElementById('guessRows');
const gameComplete = document.getElementById('gameComplete');
const successMessage = document.getElementById('successMessage');
const playButton = document.getElementById('playButton');
const replayButton = document.getElementById('replayButton');

// Load character data
async function loadCharacters() {
    try {
        const response = await fetch('database/avatar_characters.json?cacheBust=' + Date.now());
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}, URL: ${response.url}`);
        }
        const data = await response.json();
        characters = data;
        console.log("Characters loaded:", characters.length);
    } catch (error) {
        console.error('Error loading character data:', error);
    }
}


// Filter characters based on selected appearances
function getFilteredCharacters() {
    const selectedAppearances = [];

    // Shows
    if (document.getElementById('atla').checked) {
        selectedAppearances.push('Avatar: The Last Airbender');
    }
    if (document.getElementById('lok').checked) {
        selectedAppearances.push('The Legend of Korra');
    }

    // Comics (parent auto-includes children)
    if (document.getElementById('comics').checked) {
        selectedAppearances.push('Avatar Comics', 'Korra Comics');
    } else {
        if (document.getElementById('avatar-comics').checked) {
            selectedAppearances.push('Avatar Comics');
        }
        if (document.getElementById('korra-comics').checked) {
            selectedAppearances.push('Korra Comics');
        }
    }

    // Novels (parent auto-includes children)
    if (document.getElementById('novels').checked) {
        selectedAppearances.push('Kyoshi Novels', 'Yangchen Novels', 'Roku Novels', 'Avatar Novels');
    } else {
        if (document.getElementById('kyoshi-novels').checked) {
            selectedAppearances.push('Kyoshi Novels');
        }
        if (document.getElementById('yangchen-novels').checked) {
            selectedAppearances.push('Yangchen Novels');
        }
        if (document.getElementById('roku-novels').checked) {
            selectedAppearances.push('Roku Novels');
        }
        if (document.getElementById('avatar-novels').checked) {
            selectedAppearances.push('Avatar Novels');
        }
    }

    // 🔎 Debug logs
    console.log("Selected appearances:", selectedAppearances);
    console.log("Characters loaded:", characters.length);

    const filtered = characters.filter(char =>
        char.Appearances.some(appearance => selectedAppearances.includes(appearance))
    );

    console.log("Filtered characters:", filtered.length);
    return filtered;
}

// Start new game
function startGame() {
    const filteredCharacters = getFilteredCharacters();
    if (filteredCharacters.length === 0) {
        alert('Please select at least one appearance type');
        return;
    }

    targetCharacter = filteredCharacters[Math.floor(Math.random() * filteredCharacters.length)];
    guessCount = 0;
    gameActive = true;
    
    // Show/hide appropriate elements
    gameSettings.style.display = 'none';
    gameArea.style.display = 'block';
    document.querySelector('.game-instructions').style.display = 'block';
    playButton.style.display = 'none';
    characterInput.style.display = 'block';
    document.querySelector('.game-instructions').style.display = 'block';
    
    guessRows.innerHTML = '';
    gameArea.classList.remove('game-won');
    document.querySelector('.game-instructions').style.display = 'block';
    
    // Add column headers if they don't exist
    if (!document.querySelector('.column-headers')) {
        const headers = document.createElement('div');
        headers.className = 'column-headers';
        const headerNames = ['Name', 'Gender', 'Species', 'Origin', 'Bending', 'Skills', 'Affiliation', 'Appearances'];
        
        headerNames.forEach(name => {
            const header = document.createElement('div');
            header.className = 'column-header';
            header.textContent = name;
            headers.appendChild(header);
        });
        
        gameArea.insertBefore(headers, guessRows);
    }
    
    gameComplete.style.display = 'none';
    characterInput.value = '';
    characterInput.focus();

    // Move checkboxes back to settings if they were in game complete
    const checkboxContainer = document.querySelector('.checkbox-container');
    if (checkboxContainer.parentElement === gameComplete) {
        gameSettings.appendChild(checkboxContainer);
    }
}

// Handle character input and autocomplete
// Add variables for tracking selected suggestion
let currentSuggestionIndex = -1;

// Update handleInput function
function handleInput() {
    const input = characterInput.value.toLowerCase();
    autoComplete.innerHTML = '';
    currentSuggestionIndex = -1;

    if (input.length < 2) return;

    const matches = getFilteredCharacters()
        .filter(char => char.Name.toLowerCase().includes(input))
        .slice(0, 5);

    matches.forEach((char, index) => {
        const div = document.createElement('div');
        div.textContent = char.Name;
        div.setAttribute('data-index', index);
        div.addEventListener('click', () => selectSuggestion(char));
        autoComplete.appendChild(div);
    });
}

// Add keyboard navigation handling
characterInput.addEventListener('keydown', (e) => {
    const suggestions = autoComplete.children;
    if (suggestions.length === 0) return;

    if (e.key === 'Tab') {
        e.preventDefault();
        if (currentSuggestionIndex < suggestions.length - 1) {
            currentSuggestionIndex++;
        } else {
            currentSuggestionIndex = 0;
        }
        
        Array.from(suggestions).forEach((suggestion, index) => {
            if (index === currentSuggestionIndex) {
                suggestion.classList.add('selected');
                suggestion.scrollIntoView({ block: 'nearest' });
            } else {
                suggestion.classList.remove('selected');
            }
        });
    } else if (e.key === 'Enter' && currentSuggestionIndex >= 0) {
        e.preventDefault();
        const selectedChar = getFilteredCharacters()
            .filter(char => char.Name.toLowerCase().includes(characterInput.value.toLowerCase()))
            .slice(0, 5)[currentSuggestionIndex];
        if (selectedChar) {
            selectSuggestion(selectedChar);
        }
    }
});

// Add function to handle suggestion selection
function selectSuggestion(character) {
    characterInput.value = character.Name;
    autoComplete.innerHTML = '';
    currentSuggestionIndex = -1;
    handleGuess(character);
}

// Check guess against target character
function checkGuess(guess) {
    const results = {};
    
    // Compare each property
    Object.keys(guess).forEach(key => {
        if (key === 'Appearances') {
            // Check for overlap in appearances
            const intersection = guess[key].filter(x => targetCharacter[key].includes(x));
            results[key] = intersection.length > 0 ? 
                (intersection.length === guess[key].length && intersection.length === targetCharacter[key].length ? 'correct' : 'partial')
                : 'incorrect';
        } else if (key === 'Bending type') {
            // Convert to array if string
            const guessTypes = Array.isArray(guess[key]) ? guess[key] : [guess[key]];
            const targetTypes = Array.isArray(targetCharacter[key]) ? targetCharacter[key] : [targetCharacter[key]];
            
            if (guessTypes.length === targetTypes.length && 
                guessTypes.every(type => targetTypes.includes(type))) {
                results[key] = 'correct';
            } else if (guessTypes.some(type => targetTypes.includes(type))) {
                results[key] = 'partial';
            } else {
                results[key] = 'incorrect';
            }
        } else if (key === 'Affiliation/Group') {
            // Handle affiliations similar to appearances
            const intersection = guess[key].filter(x => targetCharacter[key].includes(x));
            results[key] = intersection.length > 0 ? 
                (intersection.length === guess[key].length && intersection.length === targetCharacter[key].length ? 'correct' : 'partial')
                : 'incorrect';
        } else if (Array.isArray(guess[key])) {
            // Handle other array properties
            const match = guess[key].every(item => targetCharacter[key].includes(item)) &&
                         targetCharacter[key].every(item => guess[key].includes(item));
            results[key] = match ? 'correct' : 'incorrect';
        } else {
            // Handle simple properties
            results[key] = guess[key] === targetCharacter[key] ? 'correct' : 'incorrect';
        }
    });

    return results;
}

// Display guess results
function displayGuess(character, results) {
    const row = document.createElement('div');
    row.className = 'guess-row';

    Object.entries(results).forEach(([key, result], index) => {
        if (key !== 'Image') {  // Skip the Image column
            const cell = document.createElement('div');
            cell.className = `guess-cell ${result}`;
            cell.textContent = Array.isArray(character[key]) ? 
                character[key].join(', ') : character[key];
            
            // Add delay for fade-in animation
            setTimeout(() => cell.style.opacity = 1, index * 100);
            row.appendChild(cell);
        }
    });

    // Insert at the beginning of guessRows
    guessRows.insertBefore(row, guessRows.firstChild);
    row.classList.add('show');
}

// Handle guess submission
function handleGuess(character) {
    if (!gameActive) return;

    guessCount++;
    const results = checkGuess(character);
    displayGuess(character, results);
    characterInput.value = '';

    // Check if all properties are correct
    if (Object.values(results).every(result => result === 'correct')) {
        gameActive = false;
        gameComplete.style.display = 'block';
        gameComplete.style.marginBottom = '1rem';
        successMessage.textContent = `Congratulations! You found ${targetCharacter.Name} in ${guessCount} guesses!`;
        gameArea.insertBefore(gameComplete, gameArea.firstChild);
        gameArea.classList.add('game-won');
        
        // Move checkboxes to game complete area
        const checkboxContainer = document.querySelector('.checkbox-container');
        gameComplete.appendChild(checkboxContainer);
    }
}

function setupGameControls() {
    // Create game controls container if it doesn't exist
    let gameControls = document.querySelector('.game-controls');
    if (!gameControls) {
        gameControls = document.createElement('div');
        gameControls.className = 'game-controls';
        gameArea.appendChild(gameControls);
    }

    // Add give up button
    const giveUpButton = document.createElement('button');
    giveUpButton.textContent = 'Give Up';
    giveUpButton.className = 'give-up-button';
    giveUpButton.onclick = handleGiveUp;
    gameControls.appendChild(giveUpButton);
}

// Handle give up
function handleGiveUp() {
    if (!gameActive) return;
    gameActive = false;
    gameComplete.style.display = 'block';
    gameComplete.style.marginBottom = '1rem';
    successMessage.textContent = `The character was ${targetCharacter.Name}!`;
    gameArea.classList.add('game-won');
    document.querySelector('.game-instructions').style.display = 'none';
    gameArea.insertBefore(gameComplete, gameArea.firstChild);
    gameArea.classList.add('game-won');

    // Move checkboxes to game complete area
    const checkboxContainer = document.querySelector('.checkbox-container');
    gameComplete.appendChild(checkboxContainer);
}

// Handle checkbox interactions
function setupCheckboxListeners() {
    // Comics parent-child relationship
    const comicsCheckbox = document.getElementById('comics');
    const avatarComics = document.getElementById('avatar-comics');
    const korraComics = document.getElementById('korra-comics');

    comicsCheckbox.addEventListener('change', (e) => {
        avatarComics.checked = e.target.checked;
        korraComics.checked = e.target.checked;
    });

    [avatarComics, korraComics].forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            comicsCheckbox.checked = avatarComics.checked || korraComics.checked;
        });
    });

    // Novels parent-child relationship
    const novelsCheckbox = document.getElementById('novels');
    const novelCheckboxes = [
        'kyoshi-novels',
        'yangchen-novels',
        'roku-novels',
        'avatar-novels'
    ].map(id => document.getElementById(id));

    novelsCheckbox.addEventListener('change', (e) => {
        novelCheckboxes.forEach(checkbox => checkbox.checked = e.target.checked);
    });

    novelCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            novelsCheckbox.checked = novelCheckboxes.some(cb => cb.checked);
        });
    });
}

// Initialize checkbox listeners
setupCheckboxListeners();

// Initialize game
loadCharacters();

async function initGame() {
  await loadCharacters();
  setupGameControls();
  setupCheckboxListeners();
  playButton.disabled = false;
}
initGame();

// Event listeners
playButton.addEventListener('click', startGame);
replayButton.addEventListener('click', startGame);
characterInput.addEventListener('input', handleInput);
characterInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && characterInput.value) {
        const character = getFilteredCharacters()
            .find(char => char.Name.toLowerCase() === characterInput.value.toLowerCase());
        if (character) {
            handleGuess(character);
        }
    }
});
