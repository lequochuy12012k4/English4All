// Dữ liệu flash cards
const initialCards = [
    { id: 1, word: 'Hello', meaning: 'Xin chào', example: 'Hello, how are you today?' },
    { id: 2, word: 'Goodbye', meaning: 'Tạm biệt', example: 'Goodbye, see you tomorrow!' },
    { id: 3, word: 'Thank you', meaning: 'Cảm ơn bạn', example: 'Thank you for your help.' },
    { id: 4, word: 'Sorry', meaning: 'Xin lỗi', example: 'I am sorry for the mistake.' },
    { id: 5, word: 'Friend', meaning: 'Bạn bè', example: 'She is my good friend.' },
    { id: 6, word: 'Enhance', meaning: 'Củng cố', example: 'This course will enhance your skills.' },
    { id: 7, word: 'Travel experience', meaning: 'Trải nghiệm du lịch', example: 'He shared his travel experience with us.' },
    { id: 8, word: 'Local perspective', meaning: 'Góc nhìn địa phương', example: 'A local perspective helps understand culture.' },
    { id: 9, word: 'Service', meaning: 'Dịch vụ', example: 'The hotel provides excellent service.' },
    { id: 10, word: 'Eager to', meaning: 'Háo hức, sẵn lòng làm gì', example: 'She is eager to learn new things.' },
    { id: 11, word: 'Guided tour', meaning: 'Chuyến tham quan có hướng dẫn', example: 'We booked a guided tour for the museum.' },
    { id: 12, word: 'Scenic walk', meaning: 'Đi dạo ngắm cảnh', example: 'We went on a scenic walk by the lake.' },
    { id: 13, word: 'Drop off', meaning: 'Đưa ai đó đến một nơi cụ thể', example: 'I will drop you off at the airport.' },
    { id: 14, word: 'Tourist attraction', meaning: 'Địa điểm thu hút khách du lịch', example: 'The Eiffel Tower is a famous tourist attraction.' },
    { id: 15, word: 'Explore', meaning: 'Khám phá', example: 'We love to explore new places.' },
    { id: 16, word: 'Destination', meaning: 'Điểm đến', example: 'Paris is a popular travel destination.' },
    { id: 17, word: 'Hassle', meaning: 'Khó khăn', example: 'Traveling without a visa can be a hassle.' },
    { id: 18, word: 'Like-minded', meaning: 'Có cùng trí hướng', example: 'She enjoys working with like-minded people.' },
    { id: 19, word: 'Exclusive', meaning: 'Độc nhất vô nhị', example: 'This is an exclusive offer for members.' },
    { id: 20, word: 'Marine life', meaning: 'Cuộc sống dưới biển', example: 'The coral reef is home to diverse marine life.' },
    { id: 21, word: 'Account for', meaning: 'Chiếm (bao nhiêu phần trăm)', example: 'Women account for 50% of the workforce.' },
    { id: 22, word: 'Carbon footprint', meaning: 'Dấu chân các-bon', example: 'We should reduce our carbon footprint.' },
    { id: 23, word: 'Diet', meaning: 'Chế độ ăn', example: 'A balanced diet is important for health.' },
    { id: 24, word: 'Possible', meaning: 'Có khả năng', example: 'Is it possible to finish this in a day?' },
    { id: 25, word: 'Possibility', meaning: 'Khả năng, năng lực', example: 'There is a high possibility of rain tomorrow.' },
    { id: 26, word: 'Dairy product', meaning: 'Sản phẩm làm từ sữa', example: 'Milk and cheese are dairy products.' },
    { id: 27, word: 'Consume', meaning: 'Tiêu thụ', example: 'We should consume less sugar.' }
];

// Biến trạng thái
let cards = [...initialCards];
let currentIndex = 0;
let flipped = false;
let learned = [];

// Các phần tử DOM
const cardInnerEl = document.getElementById('card-inner');
const cardWordEl = document.getElementById('card-word');
const cardMeaningEl = document.getElementById('card-meaning');
const cardExampleEl = document.getElementById('card-example');
const flipHintEl = document.getElementById('flip-hint');
const btnPrevious = document.getElementById('btn-previous');
const btnNext = document.getElementById('btn-next');
const btnLearned = document.getElementById('btn-learned');
const btnShuffle = document.getElementById('btn-shuffle');
const btnImport = document.getElementById('btn-import');
const excelInput = document.getElementById('excel-input');
const currentIndexEl = document.getElementById('current-index');
const totalCardsEl = document.getElementById('total-cards');
const progressBarEl = document.getElementById('progress-bar');
const progressTextEl = document.getElementById('progress-text');

// Hàm render card hiện tại
function renderCurrentCard() {
    const currentCard = cards[currentIndex];
    
    // Hiển thị số thẻ hiện tại và tổng số thẻ
    currentIndexEl.textContent = currentIndex + 1;
    totalCardsEl.textContent = cards.length;
    
    // Cập nhật nội dung thẻ
    cardWordEl.textContent = currentCard.word;
    cardMeaningEl.textContent = currentCard.meaning;
    cardExampleEl.textContent = currentCard.example;
    
    // Cập nhật trạng thái lật thẻ và gợi ý
    if (flipped) {
        cardInnerEl.classList.add('flipped');
        flipHintEl.textContent = 'Nhấn để xem từ';
    } else {
        cardInnerEl.classList.remove('flipped');
        flipHintEl.textContent = 'Nhấn để xem nghĩa';
    }
    
    // Cập nhật trạng thái nút
    btnPrevious.disabled = currentIndex === 0;
    btnNext.disabled = currentIndex === cards.length - 1;
    
    // Cập nhật trạng thái nút đã học
    if (learned.includes(currentCard.id)) {
        btnLearned.classList.add('active');
        btnLearned.textContent = 'Đã học';
    } else {
        btnLearned.classList.remove('active');
        btnLearned.textContent = 'Đánh dấu đã học';
    }
    
    // Cập nhật thanh tiến độ
    updateProgressBar();
}

// Cập nhật thanh tiến độ
function updateProgressBar() {
    const percentage = cards.length > 0 ? (learned.length / cards.length) * 100 : 0;
    progressBarEl.style.width = `${percentage}%`;
    progressTextEl.textContent = `${learned.length}/${cards.length} từ đã học (${Math.round(percentage)}%)`;
}

// Xử lý sự kiện lật thẻ
cardInnerEl.addEventListener('click', () => {
    flipped = !flipped;
    renderCurrentCard();
});

// Xử lý sự kiện nút trước
btnPrevious.addEventListener('click', () => {
    if (currentIndex > 0) {
        currentIndex--;
        flipped = false;
        renderCurrentCard();
    }
});

// Xử lý sự kiện nút tiếp
btnNext.addEventListener('click', () => {
    if (currentIndex < cards.length - 1) {
        currentIndex++;
        flipped = false;
        renderCurrentCard();
    }
});

// Xử lý sự kiện đánh dấu đã học
btnLearned.addEventListener('click', () => {
    const currentCard = cards[currentIndex];
    if (learned.includes(currentCard.id)) {
        learned = learned.filter(id => id !== currentCard.id);
    } else {
        learned.push(currentCard.id);
    }
    renderCurrentCard();
});

// Xử lý sự kiện xáo trộn thẻ
btnShuffle.addEventListener('click', () => {
    cards = [...cards].sort(() => Math.random() - 0.5);
    currentIndex = 0;
    flipped = false;
    renderCurrentCard();
});

// Xử lý sự kiện nhập Excel
btnImport.addEventListener('click', () => {
    excelInput.click();
});

excelInput.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: 'array' });
        const worksheet = workbook.Sheets[workbook.SheetNames[0]];
        const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

        // Chuyển đổi dữ liệu Excel
        const importedCards = jsonData.slice(1).map((row, index) => ({
            id: index + 1,
            word: row[0] || '',
            meaning: row[1] || '',
            example: row[2] || ''
        })).filter(card => card.word && card.meaning);

        if (importedCards.length > 0) {
            cards = importedCards;
            currentIndex = 0;
            learned = [];
            flipped = false;
            renderCurrentCard();
            alert(`Đã nhập thành công ${importedCards.length} thẻ!`);
        } else {
            alert('File không hợp lệ hoặc định dạng sai!');
        }
    };
    reader.readAsArrayBuffer(file);
});

// Khởi tạo hiển thị ban đầu
totalCardsEl.textContent = cards.length;
renderCurrentCard();
