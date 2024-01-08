function calculateAverage() {
    var diem15p = document.getElementsByName("diem15p")[0].value;
    var diem45p = document.getElementsByName("diem45p")[0].value;
    var diemck = document.getElementsByName("diemck")[0].value;

    // Send the data to the server for further processing
    fetch('/calculate_average', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ diem15p: diem15p, diem45p: diem45p, diemck: diemck }),
    })
    .then(response => response.json())
    .then(data => {
        alert('Average: ' + data.average);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}