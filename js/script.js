// HueBen: Xử lý logic cho Lightbox tự động nhận diện ảnh từ DOM

let currentAlbumImages = [];
let currentIndex = 0;
const lightbox = document.getElementById('lightbox');
const lightboxImg = document.getElementById('lightbox-img');

// HueBen: Hàm mở Lightbox khi click vào ảnh
function openLightbox(imgElement) {
    // Tìm phần tử chứa grid của album hiện tại
    const albumGrid = imgElement.closest('.masonry-grid');
    // Lấy tất cả các thẻ img trong album đó
    const imgs = albumGrid.querySelectorAll('img');
    
    // Chuyển danh sách img thành mảng đường dẫn (src)
    currentAlbumImages = Array.from(imgs).map(img => img.src);
    // Tìm vị trí của ảnh được click
    currentIndex = currentAlbumImages.indexOf(imgElement.src);
    
    lightboxImg.src = currentAlbumImages[currentIndex];
    lightbox.style.display = 'block';
    document.body.style.overflow = 'hidden'; // Ngăn cuộn trang bên dưới
}

// HueBen: Hàm đóng Lightbox
function closeLightbox() {
    lightbox.style.display = 'none';
    document.body.style.overflow = 'auto'; // Cho phép cuộn lại
}

// HueBen: Chuyển đổi qua lại giữa các ảnh trong cùng 1 album
function changeImage(direction) {
    currentIndex += direction;
    // Xử lý vòng lặp nếu vượt quá giới hạn mảng
    if (currentIndex >= currentAlbumImages.length) {
        currentIndex = 0;
    } else if (currentIndex < 0) {
        currentIndex = currentAlbumImages.length - 1;
    }
    
    // Thay đổi ảnh trực tiếp (xoá setTimeout để xử lý bấm/vuốt nhanh không bị lỗi hiển thị)
    lightboxImg.src = currentAlbumImages[currentIndex];
}

// HueBen: Đóng lightbox khi click ra ngoài vùng ảnh
lightbox.addEventListener('click', function(e) {
    if (e.target === lightbox) {
        closeLightbox();
    }
});

// HueBen: Hỗ trợ phím mũi tên trái/phải và Esc trên bàn phím
document.addEventListener('keydown', function(e) {
    if (lightbox.style.display === 'block') {
        if (e.key === 'ArrowLeft') {
            changeImage(-1);
        } else if (e.key === 'ArrowRight') {
            changeImage(1);
        } else if (e.key === 'Escape') {
            closeLightbox();
        }
    }
});

// HueBen: Hàm xử lý nút Xem chi tiết cho album
function toggleViewAll(btn, sectionId) {
    const grid = document.querySelector('#' + sectionId + ' .masonry-grid');
    if (grid) {
        grid.classList.toggle('show-all');
        if (grid.classList.contains('show-all')) {
            btn.innerHTML = 'Ẩn bớt';
        } else {
            btn.innerHTML = 'Xem chi tiết';
            // Tự động cuộn lại về tiêu đề album khi ẩn bớt
            const section = document.getElementById(sectionId);
            section.scrollIntoView({ behavior: 'smooth' });
        }
    }
}

// HueBen: Hỗ trợ vuốt trên điện thoại (Swipe left/right)
let touchStartX = 0;
let touchEndX = 0;

lightbox.addEventListener('touchstart', function(e) {
    touchStartX = e.changedTouches[0].screenX;
}, false);

lightbox.addEventListener('touchend', function(e) {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
}, false);

function handleSwipe() {
    // Cần một khoảng cách vuốt nhất định (50px) để tránh chạm nhầm
    if (touchStartX - touchEndX > 50) {
        changeImage(1); // Vuốt sang trái -> Ảnh tiếp theo
    }
    if (touchEndX - touchStartX > 50) {
        changeImage(-1); // Vuốt sang phải -> Ảnh trước đó
    }
}
