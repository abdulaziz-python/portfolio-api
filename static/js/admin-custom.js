/**
 * Django Unfold admin panel uchun custom javascript
 */

// DOM content yuklanganda bajariladigan funksiya
document.addEventListener('DOMContentLoaded', function() {
    // Telegraph Preview iframe uchun o'lchamni sozlaymiz
    setupTelegraphPreviews();
    
    // API so'rovlarni yaratish uchun tugmachalar
    setupApiButtons();
    
    // Telegraph ma'lumotlari uchun copy tugmachalari
    setupCopyButtons();
    
    // Admin panelga qo'shimcha CSS klasslar qo'shish
    enhanceAdminStyles();
});

/**
 * Telegraph previewlarini sozlash funktsiyasi
 * Barcha iframe elementlarini 16:9 nisbatda ko'rsatadi
 */
function setupTelegraphPreviews() {
    const iframes = document.querySelectorAll('iframe[src*="telegra.ph"]');
    iframes.forEach(iframe => {
        const container = iframe.parentElement;
        container.style.position = 'relative';
        container.style.width = '100%';
        container.style.paddingTop = '56.25%'; // 16:9 nisbat
        
        iframe.style.position = 'absolute';
        iframe.style.top = '0';
        iframe.style.left = '0';
        iframe.style.width = '100%';
        iframe.style.height = '100%';
        iframe.style.border = '1px solid #e0e0e0';
        iframe.style.borderRadius = '4px';
    });
}

/**
 * Telegraph API so'rovlari uchun tugmalar yaratish
 * So'rov natijasini chiroyli formatda ko'rsatadi
 */
function setupApiButtons() {
    const apiButtonContainers = document.querySelectorAll('.field-name:has(label:contains("Telegraph"))');
    
    apiButtonContainers.forEach(container => {
        const fieldName = container.querySelector('label').textContent.trim();
        const parent = container.closest('.form-row');
        const input = parent.querySelector('input[type="text"], textarea');
        
        if (!input) return;
        
        const buttonContainer = document.createElement('div');
        buttonContainer.classList.add('api-action-buttons');
        buttonContainer.style.marginTop = '8px';
        
        const apiButton = document.createElement('button');
        apiButton.type = 'button';
        apiButton.classList.add('button');
        apiButton.innerText = 'API orqali tekshirish';
        apiButton.style.marginRight = '8px';
        
        apiButton.addEventListener('click', async () => {
            const value = input.value.trim();
            if (!value) {
                displayMessage('Qiymat kiritilmagan', 'error');
                return;
            }
            
            try {
                apiButton.disabled = true;
                apiButton.innerText = 'Yuklanmoqda...';
                
                let url = `/api/telegraph/page-info/?path=${encodeURIComponent(value)}`;
                if (fieldName.includes('Token')) {
                    url = `/api/telegraph/pages/?token=${encodeURIComponent(value)}`;
                }
                
                const response = await fetch(url);
                const data = await response.json();
                
                const responseContainer = parent.querySelector('.api-response') || document.createElement('div');
                responseContainer.classList.add('api-response');
                responseContainer.style.marginTop = '8px';
                responseContainer.style.padding = '12px';
                responseContainer.style.backgroundColor = '#f7f7f7';
                responseContainer.style.borderRadius = '4px';
                responseContainer.style.maxHeight = '300px';
                responseContainer.style.overflow = 'auto';
                
                if (!parent.querySelector('.api-response')) {
                    parent.appendChild(responseContainer);
                }
                
                responseContainer.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
                
            } catch (error) {
                displayMessage('API so\'rovida xatolik: ' + error.message, 'error');
            } finally {
                apiButton.disabled = false;
                apiButton.innerText = 'API orqali tekshirish';
            }
        });
        
        buttonContainer.appendChild(apiButton);
        parent.appendChild(buttonContainer);
    });
}

/**
 * Telegraph URLlari uchun nusxa ko'chirish tugmalarini qo'shish
 */
function setupCopyButtons() {
    const telegraphFields = document.querySelectorAll('input[name*="telegraph_url"], input[name*="telegraph_path"]');
    
    telegraphFields.forEach(field => {
        const parent = field.parentElement;
        const copyButton = document.createElement('button');
        copyButton.type = 'button';
        copyButton.classList.add('button');
        copyButton.innerText = 'Nusxa olish';
        copyButton.style.marginLeft = '8px';
        
        copyButton.addEventListener('click', () => {
            field.select();
            document.execCommand('copy');
            
            const originalText = copyButton.innerText;
            copyButton.innerText = 'Nusxalandi!';
            copyButton.style.backgroundColor = '#4CAF50';
            copyButton.style.color = 'white';
            
            setTimeout(() => {
                copyButton.innerText = originalText;
                copyButton.style.backgroundColor = '';
                copyButton.style.color = '';
            }, 2000);
            
            displayMessage('Manzil nusxalandi!', 'success');
        });
        
        parent.appendChild(copyButton);
    });
}

/**
 * Admin paneli stillarini yaxshilash
 */
function enhanceAdminStyles() {
    // Telegraph fieldsetlarni ajratib ko'rsatish
    const fieldsets = document.querySelectorAll('fieldset');
    fieldsets.forEach(fieldset => {
        const legend = fieldset.querySelector('legend');
        if (legend && legend.textContent.includes('Telegraph')) {
            fieldset.classList.add('telegraph-fieldset');
            fieldset.style.borderLeft = '3px solid #2196F3';
            fieldset.style.backgroundColor = '#f5f9ff';
            fieldset.style.padding = '10px';
        }
    });
    
    // Django xabarlarini yaxshilash
    const messages = document.querySelectorAll('.messagelist li');
    messages.forEach(message => {
        message.style.padding = '10px 15px';
        message.style.borderRadius = '4px';
        message.style.marginBottom = '10px';
        
        if (message.classList.contains('success')) {
            message.style.backgroundColor = '#e8f5e9';
            message.style.color = '#2e7d32';
            message.style.borderLeft = '4px solid #4CAF50';
        } else if (message.classList.contains('error')) {
            message.style.backgroundColor = '#ffebee';
            message.style.color = '#c62828';
            message.style.borderLeft = '4px solid #f44336';
        }
    });
}

/**
 * Xabarlarni ko'rsatish funktsiyasi
 * 
 * @param {string} text - ko'rsatiladigan xabar
 * @param {string} type - xabar turi (success, error, info)
 */
function displayMessage(text, type = 'info') {
    const messagesList = document.querySelector('.messagelist') || createMessagesList();
    
    const message = document.createElement('li');
    message.classList.add(type);
    message.textContent = text;
    
    // Stil qo'shish
    message.style.padding = '10px 15px';
    message.style.borderRadius = '4px';
    message.style.marginBottom = '10px';
    
    if (type === 'success') {
        message.style.backgroundColor = '#e8f5e9';
        message.style.color = '#2e7d32';
        message.style.borderLeft = '4px solid #4CAF50';
    } else if (type === 'error') {
        message.style.backgroundColor = '#ffebee';
        message.style.color = '#c62828';
        message.style.borderLeft = '4px solid #f44336';
    } else {
        message.style.backgroundColor = '#e3f2fd';
        message.style.color = '#1565c0';
        message.style.borderLeft = '4px solid #2196F3';
    }
    
    messagesList.appendChild(message);
    
    // 5 soniyadan keyin o'chirish
    setTimeout(() => {
        message.style.opacity = '0';
        message.style.transition = 'opacity 0.5s';
        
        setTimeout(() => {
            message.remove();
            if (messagesList.children.length === 0) {
                messagesList.remove();
            }
        }, 500);
    }, 5000);
}

/**
 * Xabarlar ro'yxatini yaratish
 */
function createMessagesList() {
    const container = document.querySelector('#container');
    const content = document.querySelector('#content');
    
    const messagesList = document.createElement('ul');
    messagesList.classList.add('messagelist');
    
    container.insertBefore(messagesList, content);
    return messagesList;
}

/**
 * CSRF token ni cookie-dan olish
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
} 