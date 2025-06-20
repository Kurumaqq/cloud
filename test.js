let a = ['rock', 'paper', 'scissors'];
b = '';
function scissors() {
    a.forEach((item, index) => {
        b += `<p>${index + 1}. ${item}</p>`;
    });
    document.querySelector('.hui').innerHTML = b;
}
