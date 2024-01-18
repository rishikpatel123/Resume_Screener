function screenResumes() {
    const resumeInput = document.getElementById('resumeInput');
    const keywordInput = document.getElementById('keywordInput');
    const resultsContainer = document.getElementById('results');

    const selectedResumes = [];

    for (const file of resumeInput.files) {
        
        const reader = new FileReader();
        reader.onload = function (event) {
            const resumeContent = event.target.result;


            if (resumeContent.includes(keywordInput.value)) {
                selectedResumes.push(file.name);
            }


            resultsContainer.innerHTML = `Selected Resumes: ${selectedResumes.join(', ')}`;
        };

        reader.readAsText(file);
    }


    if (selectedResumes.length > 0) {
        const shortlistedNames = selectedResumes.join(', ');
        openModal(`Shortlisted Resumes: ${shortlistedNames}`);
    } else {
        openModal('No resumes match the specified criteria.');
    }

    return false; 
}
