async function analyzeText() {
    const text = document.getElementById('textInput').value;

    if (!text) {
        alert('Please enter some text to analyze.');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Error analyzing text:', error);
        document.getElementById('result').innerText = 'Failed to analyze text. Please try again.';
    }
}

function displayResults(data) {
    const resultDiv = document.getElementById('result');
    if (data.sentiment && data.confidence_scores) {
        resultDiv.innerHTML = `
            <h2>Analysis Results</h2>
            <p><strong>Sentiment:</strong> ${data.sentiment}</p>
            <p><strong>Confidence Scores:</strong></p>
            <ul>
                <li>Positive: ${data.confidence_scores.positive.toFixed(2)}</li>
                <li>Neutral: ${data.confidence_scores.neutral.toFixed(2)}</li>
                <li>Negative: ${data.confidence_scores.negative.toFixed(2)}</li>
            </ul>
        `;
    } else {
        resultDiv.innerText = 'No analysis results available.';
    }
}