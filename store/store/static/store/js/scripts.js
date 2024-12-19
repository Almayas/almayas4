// Custom JavaScript for Almayas4

// Example: Confirm before removing an item from the cart
document.addEventListener('DOMContentLoaded', function() {
    const removeButtons = document.querySelectorAll('.btn-danger');
    removeButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            if(!confirm('Are you sure you want to remove this item from your cart?')) {
                event.preventDefault();
            }
        });
    });
});
