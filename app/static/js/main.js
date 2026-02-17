// Heaven Bookstore - JavaScript Functionality

$(document).ready(function() {
    
    // ========== AJAX Add to Cart ==========
    $('.add-to-cart-btn').on('click', function(e) {
        e.preventDefault();
        
        const bookId = $(this).data('book-id');
        const button = $(this);
        
        // Disable button during request
        button.prop('disabled', true);
        const originalText = button.html();
        button.html('<i class="fas fa-spinner fa-spin"></i> Adding...');
        
        $.ajax({
            url: `/cart/add/${bookId}`,
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')
            },
            // Get CSRF token from hidden field if meta tag not available
            beforeSend: function(xhr) {
                const token = $('input[name="csrf_token"]').val();
                if (token) {
                    xhr.setRequestHeader('X-CSRFToken', token);
                }
            },
            success: function(response) {
                if (response.success) {
                    // Update cart count
                    $('#cart-count').text(response.cart_count);
                    
                    // Show success message
                    showToast('success', response.message || 'Book added to cart!');
                    
                    // Reset button
                    button.html('<i class="fas fa-check"></i> Added!');
                    setTimeout(function() {
                        button.html(originalText);
                        button.prop('disabled', false);
                    }, 2000);
                }
            },
            error: function(xhr) {
                // Show error message
                showToast('danger', 'Failed to add book to cart. Please try again.');
                
                // Reset button
                button.html(originalText);
                button.prop('disabled', false);
            }
        });
    });
    
    
    // ========== Toast Notification Function ==========
    function showToast(type, message) {
        const toast = $(`
            <div class="alert alert-${type} alert-dismissible fade show position-fixed" 
                 style="top: 100px; right: 20px; z-index: 9999; min-width: 300px;" 
                 role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `);
        
        $('body').append(toast);
        
        // Auto dismiss after 3 seconds
        setTimeout(function() {
            toast.alert('close');
        }, 3000);
    }
    
    
    // ========== Star Rating Selector ==========
    $('.star-rating').each(function() {
        const container = $(this);
        const input = container.find('input[type="hidden"]');
        const stars = container.find('.star');
        
        stars.on('click', function() {
            const rating = $(this).data('rating');
            input.val(rating);
            
            // Update star display
            stars.each(function() {
                const starRating = $(this).data('rating');
                if (starRating <= rating) {
                    $(this).removeClass('far').addClass('fas');
                } else {
                    $(this).removeClass('fas').addClass('far');
                }
            });
        });
        
        stars.on('mouseenter', function() {
            const rating = $(this).data('rating');
            stars.each(function() {
                const starRating = $(this).data('rating');
                if (starRating <= rating) {
                    $(this).addClass('hover');
                }
            });
        });
        
        stars.on('mouseleave', function() {
            stars.removeClass('hover');
        });
    });
    
    
    // ========== Smooth Scroll for Anchor Links ==========
    $('a[href^="#"]').on('click', function(e) {
        const target = $(this.getAttribute('href'));
        if (target.length) {
            e.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 100
            }, 600);
        }
    });
    
    
    // ========== Form Validation Enhancement ==========
    $('form').on('submit', function() {
        const submitBtn = $(this).find('button[type="submit"]');
        const originalText = submitBtn.html();
        
        // Disable button and show loading state
        submitBtn.prop('disabled', true);
        submitBtn.html('<i class="fas fa-spinner fa-spin"></i> Processing...');
        
        // Re-enable after a delay if form validation fails
        setTimeout(function() {
            if (!submitBtn.prop('disabled')) {
                submitBtn.html(originalText);
            }
        }, 3000);
    });
    
    
    // ========== Image Lazy Loading ==========
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[loading="lazy"]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    
    // ========== Auto-dismiss Alerts ==========
    $('.alert').each(function() {
        const alert = $(this);
        setTimeout(function() {
            alert.fadeOut('slow', function() {
                alert.remove();
            });
        }, 5000);
    });
    
    
    // ========== Search Input Focus ==========
    $('.search-form input').on('focus', function() {
        $(this).parent().addClass('focused');
    }).on('blur', function() {
        $(this).parent().removeClass('focused');
    });
    
    
    // ========== Back to Top Button (Optional) ==========
    const backToTopBtn = $('<button class="back-to-top" title="Back to Top"><i class="fas fa-arrow-up"></i></button>');
    $('body').append(backToTopBtn);
    
    backToTopBtn.on('click', function() {
        $('html, body').animate({ scrollTop: 0 }, 600);
    });
    
    $(window).on('scroll', function() {
        if ($(this).scrollTop() > 300) {
            backToTopBtn.fadeIn();
        } else {
            backToTopBtn.fadeOut();
        }
    });
    
    // Style for back to top button
    $('<style>')
        .text(`
            .back-to-top {
                position: fixed;
                bottom: 30px;
                right: 30px;
                background-color: #8D6E63;
                color: white;
                border: none;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                font-size: 1.2rem;
                cursor: pointer;
                display: none;
                z-index: 1000;
                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
            }
            .back-to-top:hover {
                background-color: #6D4C41;
                transform: translateY(-3px);
            }
        `)
        .appendTo('head');
    
    
    // ========== Confirmation for Destructive Actions ==========
    $('button[data-confirm], a[data-confirm]').on('click', function(e) {
        const message = $(this).data('confirm');
        if (!confirm(message)) {
            e.preventDefault();
        }
    });
    
});
