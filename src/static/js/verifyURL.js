function checkURL(){
    const url = document.querySelector('#urlVerify').value;
    document.querySelector('#loading').classList.remove('hidden');
    emitData('checkURL', url);
}

function checkResults(result){
    let resultsDiv = document.querySelector('#checkResults');
    if(result[0] == '0'){
        resultsDiv.querySelector('img').src = "../static/images/check.svg"
    }
    else{
        resultsDiv.querySelector('img').src = "../static/images/close.svg"
    }
    resultsDiv.querySelector('p').textContent = result.substring(1);
    resultsDiv.classList.remove('hidden');
    document.querySelector('#loading').classList.add('hidden');
}