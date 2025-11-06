// Frontend JavaScript for Traveller's Assistant

const API_BASE_URL = 'http://localhost:5000/api';

// Elements
const travelForm = document.getElementById('travelForm');
const inputSection = document.getElementById('inputSection');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const newPlanBtn = document.getElementById('newPlanBtn');

// Set min date to today
document.getElementById('startDate').min = new Date().toISOString().split('T')[0];
document.getElementById('endDate').min = new Date().toISOString().split('T')[0];

// Form submission
travelForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Hide error
    errorSection.classList.add('hidden');
    
    // Collect form data
    const formData = collectFormData();
    
    // Validate dates
    if (new Date(formData.dates.start) > new Date(formData.dates.end)) {
        showError('End date must be after start date');
        return;
    }
    
    // Show loading
    inputSection.classList.add('hidden');
    resultsSection.classList.add('hidden');
    loadingSection.classList.remove('hidden');
    
    try {
        // Call API
        const response = await fetch(`${API_BASE_URL}/generate-plan`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Display results
        displayResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to generate travel plan. Please check your API configuration and try again.');
        loadingSection.classList.add('hidden');
        inputSection.classList.remove('hidden');
    }
});

// New plan button
newPlanBtn.addEventListener('click', () => {
    resultsSection.classList.add('hidden');
    inputSection.classList.remove('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

function collectFormData() {
    // Get food preferences
    const foodPrefs = [];
    document.querySelectorAll('.food-pref:checked').forEach(checkbox => {
        foodPrefs.push(checkbox.value);
    });
    
    const otherPrefs = document.getElementById('otherFoodPrefs').value.trim();
    if (otherPrefs) {
        foodPrefs.push(otherPrefs);
    }
    
    return {
        destination: document.getElementById('destination').value,
        dates: {
            start: document.getElementById('startDate').value,
            end: document.getElementById('endDate').value
        },
        purpose: document.getElementById('purpose').value,
        travelers: {
            type: document.getElementById('travelerType').value,
            count: parseInt(document.getElementById('travelerCount').value),
            composition: document.getElementById('groupComposition').value || '',
            age_range: 'Not specified'
        },
        food_preferences: foodPrefs,
        accommodation: {
            type: document.getElementById('accommodationType').value,
            location: document.getElementById('accommodationLocation').value,
            budget: document.getElementById('accommodationBudget').value
        },
        specific_questions: document.getElementById('specificQuestions').value
    };
}

function displayResults(data) {
    // Hide loading
    loadingSection.classList.add('hidden');
    
    // Show results
    resultsSection.classList.remove('hidden');
    
    // Display weather
    displayWeather(data.weather);
    
    // Display advice sections
    displayAdvice(data.advice, data.country);
    
    // Scroll to results
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function displayWeather(weatherData) {
    const weatherCard = document.getElementById('weatherCard');
    
    if (!weatherData || !weatherData.forecast) {
        weatherCard.innerHTML = '<p class="text-gray-600">Weather data not available</p>';
        return;
    }
    
    let html = `
        <h2 class="text-xl font-bold text-gray-800 mb-3">🌤️ Weather Forecast</h2>
        <p class="text-gray-600 mb-4">${weatherData.summary}</p>
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
    `;
    
    weatherData.forecast.forEach(day => {
        html += `
            <div class="bg-blue-50 rounded-lg p-3 text-center">
                <p class="font-semibold text-gray-800 text-sm">${day.day}</p>
                <p class="text-xs text-gray-600">${day.date}</p>
                <p class="text-2xl my-2">${getWeatherEmoji(day.condition)}</p>
                <p class="text-sm text-gray-700">${day.temp_max}° / ${day.temp_min}°C</p>
                <p class="text-xs text-gray-600 capitalize">${day.condition}</p>
                ${day.rain_chance > 30 ? `<p class="text-xs text-blue-600 mt-1">💧 ${day.rain_chance}%</p>` : ''}
            </div>
        `;
    });
    
    html += '</div>';
    weatherCard.innerHTML = html;
}

function displayAdvice(advice, countryData) {
    const container = document.getElementById('adviceContainer');
    
    const sections = [
        { key: 'accommodation', title: '🏨 Accommodation', icon: '🏨' },
        { key: 'currency_payments', title: '💰 Currency & Payments', icon: '💰' },
        { key: 'transportation', title: '🚗 Transportation', icon: '🚗' },
        { key: 'cultural_guide', title: '🌍 Cultural Guide', icon: '🌍' },
        { key: 'food_dining', title: '🍽️ Food & Dining', icon: '🍽️' },
        { key: 'activities', title: '🎯 Activities & Attractions', icon: '🎯' },
        { key: 'practical_info', title: '🔌 Practical Information', icon: '🔌' },
        { key: 'packing', title: '🎒 Packing List', icon: '🎒' },
        { key: 'safety_health', title: '⚕️ Safety & Health', icon: '⚕️' }
    ];
    
    if (advice.specific_answers && advice.specific_answers.trim()) {
        sections.push({ key: 'specific_answers', title: '❓ Your Questions Answered', icon: '❓' });
    }
    
    let html = '';
    
    sections.forEach(section => {
        const content = advice[section.key];
        if (content && content.trim()) {
            html += `
                <div class="bg-white rounded-lg shadow-md p-6">
                    <h3 class="text-lg font-bold text-gray-800 mb-3 flex items-center">
                        <span class="text-2xl mr-2">${section.icon}</span>
                        ${section.title}
                    </h3>
                    <div class="prose prose-sm max-w-none text-gray-700">
                        ${formatAdviceContent(content)}
                    </div>
                    ${section.key === 'practical_info' && advice.power_adapter ? formatPowerAdapterInfo(advice.power_adapter) : ''}
                </div>
            `;
        }
    });
    
    // Add country quick facts
    if (countryData) {
        html = `
            <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg shadow-md p-6">
                <h3 class="text-lg font-bold text-gray-800 mb-3">📍 Quick Facts</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                    <div><strong>Capital:</strong> ${countryData.capital}</div>
                    <div><strong>Currency:</strong> ${countryData.currency}</div>
                    <div><strong>Languages:</strong> ${countryData.languages.join(', ')}</div>
                    <div><strong>Timezone:</strong> ${countryData.timezone}</div>
                    ${countryData.calling_code ? `<div><strong>Calling Code:</strong> ${countryData.calling_code}</div>` : ''}
                    ${countryData.driving_side ? `<div><strong>Driving Side:</strong> ${countryData.driving_side}</div>` : ''}
                </div>
            </div>
        ` + html;
    }
    
    container.innerHTML = html;
}

function formatAdviceContent(content) {
    // Convert markdown-style formatting to HTML
    content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    content = content.replace(/\n\n/g, '</p><p>');
    content = content.replace(/\n- /g, '<br>• ');
    content = content.replace(/\n/g, '<br>');

    return `<p>${content}</p>`;
}

function formatPowerAdapterInfo(adapterInfo) {
    console.log('NEW VERSION 2.0 - Power adapter data:', adapterInfo);
    if (!adapterInfo || !adapterInfo.types || adapterInfo.types.length === 0) {
        return '';
    }

    let html = '<div class="mt-6 p-6 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg border-2 border-blue-300 shadow-lg">';
    html += '<h4 class="font-bold text-xl text-gray-800 mb-4 flex items-center">';
    html += '<span class="text-3xl mr-3">🔌</span> Power Adapter Visual Guide';
    html += '</h4>';
    html += '<p class="text-sm text-gray-600 mb-4">You will need the following power adapter type(s) for this destination:</p>';
    html += '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">';

    adapterInfo.types.forEach(adapter => {
        const prongIcon = '●'.repeat(adapter.prongs || 2);
        const groundedBadge = adapter.grounded ? '<span class="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">Grounded</span>' : '<span class="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">Not Grounded</span>';

        html += `
            <div class="bg-white rounded-lg p-6 shadow-md border-2 border-gray-200 hover:border-blue-400 transition-all hover:shadow-xl">
                <div class="text-center mb-4">
                    <span class="inline-block bg-gradient-to-r from-blue-600 to-blue-700 text-white font-bold text-4xl px-8 py-4 rounded-xl shadow-lg">
                        Type ${adapter.type}
                    </span>
                </div>

                <!-- Visual representation -->
                <div class="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-8 mb-4 border-2 border-gray-300 shadow-inner">
                    <div class="text-center mb-4">
                        <div class="text-7xl mb-2">🔌</div>
                        <div class="text-5xl text-gray-600 font-mono tracking-wider">${prongIcon}</div>
                        <div class="text-xs text-gray-500 mt-2">${adapter.prongs} Prongs</div>
                    </div>
                    <div class="bg-white rounded-lg p-4 text-center shadow">
                        <p class="text-sm font-semibold text-gray-800 mb-1">${adapter.shape}</p>
                        <p class="text-lg font-bold text-blue-600">${adapter.voltage}</p>
                    </div>
                </div>

                <!-- Details -->
                <div class="space-y-2 mb-4">
                    <div class="flex justify-between items-center p-2 bg-gray-50 rounded">
                        <span class="text-sm text-gray-600">Shape:</span>
                        <span class="text-sm font-semibold text-gray-800">${adapter.shape}</span>
                    </div>
                    <div class="flex justify-between items-center p-2 bg-gray-50 rounded">
                        <span class="text-sm text-gray-600">Voltage:</span>
                        <span class="text-sm font-semibold text-gray-800">${adapter.voltage}</span>
                    </div>
                    <div class="flex justify-between items-center p-2 bg-gray-50 rounded">
                        <span class="text-sm text-gray-600">Status:</span>
                        ${groundedBadge}
                    </div>
                </div>

                ${adapter.countries ? `
                <div class="pt-4 border-t border-gray-200">
                    <p class="text-xs text-gray-500 text-center">
                        <strong>Common in:</strong> ${adapter.countries}
                    </p>
                </div>
                ` : ''}
            </div>
        `;
    });

    html += '</div>';
    html += '<div class="mt-6 p-4 bg-yellow-50 border-2 border-yellow-300 rounded-lg text-sm text-gray-700">';
    html += '<strong>💡 Pro Tip:</strong> Consider buying a universal travel adapter that supports multiple plug types! This is more convenient than carrying multiple adapters.';
    html += '</div>';
    html += '</div>';

    return html;
}

function getWeatherEmoji(condition) {
    condition = condition.toLowerCase();
    
    if (condition.includes('rain') || condition.includes('drizzle')) return '🌧️';
    if (condition.includes('snow')) return '❄️';
    if (condition.includes('cloud')) return '☁️';
    if (condition.includes('clear') || condition.includes('sun')) return '☀️';
    if (condition.includes('thunder') || condition.includes('storm')) return '⛈️';
    if (condition.includes('mist') || condition.includes('fog')) return '🌫️';
    
    return '🌤️';
}

function showError(message) {
    errorMessage.textContent = message;
    errorSection.classList.remove('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Auto-update end date when start date changes
document.getElementById('startDate').addEventListener('change', (e) => {
    const startDate = new Date(e.target.value);
    const endDateInput = document.getElementById('endDate');
    
    // Set end date minimum to start date
    endDateInput.min = e.target.value;
    
    // If end date is before start date, update it
    if (endDateInput.value && new Date(endDateInput.value) < startDate) {
        // Set end date to 7 days after start
        const suggestedEnd = new Date(startDate);
        suggestedEnd.setDate(suggestedEnd.getDate() + 7);
        endDateInput.value = suggestedEnd.toISOString().split('T')[0];
    }
});
