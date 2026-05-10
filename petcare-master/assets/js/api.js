/* =====================================================================
   api.js — shared helpers for all petcare pages
   Change API_BASE to match your server address.
   ===================================================================== */

const API_BASE = '/api/v1';

async function apiFetch(path) {
    try {
        const res = await fetch(API_BASE + path);
        if (!res.ok) return null;
        const json = await res.json();
        return json.data ?? json.results ?? json;
    } catch (e) {
        console.warn('API fetch failed:', path, e);
        return null;
    }
}

function fmtDate(iso) {
    if (!iso) return '';
    const d = new Date(iso);
    return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

function imgOrPlaceholder(url, fallback) {
    return url || fallback || 'assets/img/gallery/blog1.png';
}

/* Load contact info into footer + header phone */
async function loadContactGlobal() {
    const info = await apiFetch('/contact/info/');
    if (!info) return;
    document.querySelectorAll('.js-contact-phone').forEach(el => {
        el.textContent = info.phone;
        el.href = 'tel:' + info.phone.replace(/\s/g, '');
    });
    document.querySelectorAll('.js-contact-email').forEach(el => {
        el.textContent = info.email;
        el.href = 'mailto:' + info.email;
    });
    document.querySelectorAll('.js-contact-address').forEach(el => {
        el.textContent = info.address;
    });
    document.querySelectorAll('.js-working-hours').forEach(el => {
        el.textContent = info.working_hours;
    });
}
