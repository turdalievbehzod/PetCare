/* =========================================================
   api.js — shared helpers for all PetCare pages
   ========================================================= */

const API_BASE = '/api/v1';

/* Read the Django CSRF token from the cookie (safe to call even if absent) */
function getCsrfToken() {
    const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : '';
}

/* POST JSON to an API endpoint — returns { ok, status, data } */
async function postJSON(path, body) {
    try {
        const res = await fetch(API_BASE + path, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify(body),
        });
        const json = await res.json();
        return { ok: res.ok, status: res.status, data: json };
    } catch (e) {
        console.warn('postJSON failed:', path, e);
        return { ok: false, status: 0, data: null };
    }
}

/* Generic fetch that unwraps {data:...} or {results:...} */
async function apiFetch(path) {
    try {
        const res = await fetch(API_BASE + path);
        if (!res.ok) return null;
        const json = await res.json();
        return json.data ?? json.results ?? json;
    } catch (e) {
        console.warn('apiFetch failed:', path, e);
        return null;
    }
}

/* Raw fetch — returns full JSON body (used when pagination object is needed) */
async function apiFetchRaw(path) {
    try {
        const res = await fetch(API_BASE + path);
        if (!res.ok) return null;
        return await res.json();
    } catch (e) {
        console.warn('apiFetchRaw failed:', path, e);
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

/* ---- Auth buttons (desktop + mobile) ---- */
function initAuthButtons() {
    const container = document.getElementById('auth-buttons');
    const token = localStorage.getItem('access_token');

    if (token) {
        if (container) {
            container.innerHTML = '<a href="#" class="header-btn js-logout">Logout</a>';
        }
        _injectMobileAuth('<a href="#" class="slicknav-auth-link js-logout">Logout</a>');
    } else {
        if (container) {
            container.innerHTML =
                '<a href="login.html" class="header-btn mr-2">Login</a>' +
                '<a href="register.html" class="header-btn">Register</a>';
        }
        _injectMobileAuth(
            '<a href="login.html" class="slicknav-auth-link">Login</a>' +
            '<a href="register.html" class="slicknav-auth-link">Register</a>'
        );
    }

    /* Event delegation covers both desktop and mobile logout buttons */
    document.addEventListener('click', function (e) {
        if (e.target.closest('.js-logout')) {
            e.preventDefault();
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.reload();
        }
    });
}

/* Append auth links to the slicknav mobile menu */
function _injectMobileAuth(html) {
    /* One-time style injection for mobile auth row */
    if (!document.getElementById('_sa-css')) {
        var s = document.createElement('style');
        s.id = '_sa-css';
        s.textContent =
            '.slicknav-auth-row{background:#444;padding:6px 10px;text-align:left;}' +
            '.slicknav-auth-link{display:inline-block;padding:5px 14px;margin:3px 4px;' +
            'background:#3eb489;color:#fff!important;border-radius:3px;font-size:13px;' +
            'text-decoration:none;transition:background .2s;}' +
            '.slicknav-auth-link:hover,.slicknav-auth-link:focus{background:#2d9a6e;color:#fff!important;}';
        document.head.appendChild(s);
    }

    var mobileMenu = document.querySelector('.mobile_menu');
    if (!mobileMenu) return;
    var row = mobileMenu.querySelector('.slicknav-auth-row');
    if (!row) {
        row = document.createElement('div');
        row.className = 'slicknav-auth-row';
        mobileMenu.appendChild(row);
    }
    row.innerHTML = html;
}

/* ---- Contact info: populate js-contact-* elements ---- */
async function loadContactGlobal() {
    const info = await apiFetch('/contact/info/');
    if (!info) return;

    document.querySelectorAll('.js-contact-phone').forEach(el => {
        el.textContent = info.phone || '';
        if (el.tagName === 'A') el.href = 'tel:' + (info.phone || '').replace(/\s/g, '');
    });
    document.querySelectorAll('.js-contact-email').forEach(el => {
        el.textContent = info.email || '';
        if (el.tagName === 'A') el.href = 'mailto:' + (info.email || '');
    });
    document.querySelectorAll('.js-contact-address').forEach(el => {
        el.textContent = info.address || '';
    });
    document.querySelectorAll('.js-working-hours').forEach(el => {
        el.textContent = info.working_hours || '';
    });

    /* Map iframe */
    const mapEl = document.getElementById('contact-map-iframe');
    if (mapEl && info.map_embed_url) {
        mapEl.src = info.map_embed_url;
        const wrap = mapEl.closest('.map-wrapper');
        if (wrap) wrap.style.display = '';
    }

    /* Social links — update any [data-social] anchors */
    const socialMap = {
        facebook: info.facebook_url,
        twitter:  info.twitter_url,
        linkedin: info.linkedin_url,
        instagram: info.instagram_url,
    };
    Object.keys(socialMap).forEach(function (platform) {
        const url = socialMap[platform];
        document.querySelectorAll('[data-social="' + platform + '"]').forEach(function (el) {
            if (url) { el.href = url; } else { el.style.display = 'none'; }
        });
    });
}

/* ---- Footer dynamic content ---- */
async function loadFooter() {
    await loadContactGlobal();

    /* Footer services list */
    const footerSvc = document.getElementById('footer-services');
    if (footerSvc) {
        const services = await apiFetch('/services/');
        if (services && services.length) {
            footerSvc.innerHTML = services
                .slice(0, 5)
                .map(s => `<li><a href="services.html">${escHtml(s.title)}</a></li>`)
                .join('');
        }
    }

    /* Footer about blurb */
    const footerDesc = document.getElementById('footer-desc');
    if (footerDesc) {
        const about = await apiFetch('/about/');
        if (about && (about.commitment_description || about.mission_content)) {
            const text = about.commitment_description || about.mission_content || '';
            footerDesc.textContent = text.length > 120 ? text.slice(0, 120) + '…' : text;
        }
    }
}

/* ---- Blog sidebar helpers ---- */
async function loadBlogSidebar(activeCategorySlug) {
    /* Categories */
    const catList = document.getElementById('sidebar-categories');
    if (catList) {
        const cats = await apiFetch('/blogs/categories/');
        if (cats && cats.length) {
            catList.innerHTML = cats.map(c => {
                const active = c.slug === activeCategorySlug ? ' style="font-weight:bold"' : '';
                return `<li><a href="blog.html?category=${c.slug}" class="d-flex"${active}><p>${escHtml(c.name)}</p></a></li>`;
            }).join('');
        } else {
            catList.innerHTML = '<li><p class="text-muted">No categories yet.</p></li>';
        }
    }

    /* Recent posts */
    const recentList = document.getElementById('sidebar-recent');
    if (recentList) {
        const raw = await apiFetchRaw('/blogs/?page_size=4');
        const posts = raw && raw.results ? raw.results : (Array.isArray(raw) ? raw : []);
        if (posts.length) {
            recentList.innerHTML = posts.map(p => `
                <div class="media post_item">
                    <img src="${imgOrPlaceholder(p.cover_image_url, 'assets/img/post/post_1.png')}" alt="${escHtml(p.title)}" style="width:75px;height:60px;object-fit:cover">
                    <div class="media-body">
                        <a href="blog_details.html?slug=${encodeURIComponent(p.slug)}">
                            <h3>${escHtml(p.title)}</h3>
                        </a>
                        <p>${fmtDate(p.published_at || p.created_at)}</p>
                    </div>
                </div>`).join('');
        } else {
            recentList.innerHTML = '<p class="text-muted">No posts yet.</p>';
        }
    }

    /* Tags */
    const tagList = document.getElementById('sidebar-tags');
    if (tagList) {
        const tags = await apiFetch('/blogs/tags/');
        if (tags && tags.length) {
            tagList.innerHTML = tags.map(t =>
                `<li><a href="blog.html?tag=${encodeURIComponent(t)}">${escHtml(t)}</a></li>`
            ).join('');
        } else {
            tagList.innerHTML = '<li><a href="blog.html">All Posts</a></li>';
        }
    }
}

/* ---- Service card renderer (reusable across pages) ---- */
function renderServiceCard(s, opts) {
    opts = opts || {};
    const featured = opts.featured || false;
    const media = s.image_url
        ? `<img src="${escHtml(s.image_url)}" alt="${escHtml(s.title)}" loading="lazy" onerror="this.parentNode.innerHTML='<div class=svc-icon-fallback><span class=\\'${escHtml(s.icon_class || 'flaticon-animal-kingdom')}\\'></span></div>'">`
        : `<div class="services-ion"><span class="${escHtml(s.icon_class || 'flaticon-animal-kingdom')}"></span></div>`;
    const badge = s.category_name
        ? `<span class="svc-cat-badge">${escHtml(s.category_name)}</span>`
        : '';
    const featuredClass = featured ? ' svc-featured-card' : '';
    return `
        <div class="col-lg-4 col-md-6 col-sm-6">
            <div class="single-services text-center mb-30${featuredClass}">
                ${media}
                <div class="services-cap">
                    ${badge}
                    <h5><a href="services.html">${escHtml(s.title)}</a></h5>
                    <p>${escHtml(s.description)}</p>
                </div>
            </div>
        </div>`;
}

/* ---- Simple HTML escaping ---- */
function escHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;')
              .replace(/</g, '&lt;')
              .replace(/>/g, '&gt;')
              .replace(/"/g, '&quot;');
}

/* ---- About page render helpers ---- */

function renderStats(stats) {
    const container = document.getElementById('about-stats');
    if (!container || !stats) return;

    const items = [
        { value: stats.successful_treatments, label: stats.successful_treatments_label || 'Successful Treatments', icon: 'fa-stethoscope' },
        { value: stats.happy_clients,         label: stats.happy_clients_label || 'Happy Clients',            icon: 'fa-heart' },
        { value: stats.veterinarians,         label: 'Veterinarians',                                          icon: 'fa-user-md' },
        { value: stats.years_experience,      label: 'Years Experience',                                       icon: 'fa-award' },
        { value: stats.appointments_count,    label: 'Appointments',                                           icon: 'fa-calendar-check' },
    ];

    container.innerHTML = items.map(item => `
        <div class="col-lg-2 col-md-4 col-6 mb-30">
            <div class="single-counter text-center">
                <i class="fas ${escHtml(item.icon)} fa-2x mb-2" style="color:#3eb489"></i>
                <h2>${item.value || 0}</h2>
                <p>${escHtml(item.label)}</p>
            </div>
        </div>`).join('');
}

function renderTeam(members) {
    const container = document.getElementById('team-grid');
    if (!container) return;
    if (!members || !members.length) {
        container.innerHTML = '<p class="col-12 text-center text-muted py-5">Team information coming soon.</p>';
        return;
    }
    container.innerHTML = members.map(m => `
        <div class="col-xl-4 col-lg-4 col-md-6 mb-30">
            <div class="single-team">
                <div class="team-img">
                    <img src="${escHtml(imgOrPlaceholder(m.photo_url, 'assets/img/gallery/team1.png'))}"
                         alt="${escHtml(m.name)}" loading="lazy"
                         onerror="this.src='assets/img/gallery/team1.png'">
                </div>
                <div class="team-caption">
                    <span>${escHtml(m.title || '')}</span>
                    <h3><a href="#">${escHtml(m.name)}</a></h3>
                    ${m.bio ? `<p class="team-bio" style="font-size:13px;color:#888;margin-top:6px">${escHtml(m.bio)}</p>` : ''}
                </div>
            </div>
        </div>`).join('');
}

function renderTestimonials(testimonials) {
    const section = document.getElementById('testimonials-section');
    const container = document.getElementById('testimonials-container');
    if (!container) return;
    if (!testimonials || !testimonials.length) {
        if (section) section.style.display = 'none';
        return;
    }
    if (section) section.style.display = '';
    container.innerHTML = testimonials.map(t => {
        const r = Math.min(5, Math.max(1, t.rating || 5));
        const stars = '<i class="fas fa-star" style="color:#f5a623"></i>'.repeat(r) +
                      '<i class="far fa-star" style="color:#ddd"></i>'.repeat(5 - r);
        return `
            <div class="col-xl-4 col-lg-4 col-md-6 mb-30">
                <div class="single-testimonial" style="background:#fff;border-radius:8px;padding:28px;box-shadow:0 2px 16px rgba(0,0,0,.06)">
                    <div class="mb-3">${stars}</div>
                    <p style="color:#555;font-size:15px;line-height:1.7">&ldquo;${escHtml(t.text || '')}&rdquo;</p>
                    <div class="testimonial-founder d-flex align-items-center mt-20">
                        <div class="founder-img mr-3">
                            <img src="${escHtml(imgOrPlaceholder(t.avatar_url, 'assets/img/gallery/team1.png'))}"
                                 alt="${escHtml(t.name)}" loading="lazy"
                                 style="width:48px;height:48px;border-radius:50%;object-fit:cover">
                        </div>
                        <div class="founder-text">
                            <strong style="display:block">${escHtml(t.name || '')}</strong>
                        </div>
                    </div>
                </div>
            </div>`;
    }).join('');
}

function renderRecentBlogs(posts) {
    const container = document.getElementById('recent-blogs-grid');
    if (!container) return;
    if (!posts || !posts.length) {
        container.closest('.home_blog-area') && (container.closest('.home_blog-area').style.display = 'none');
        return;
    }
    container.innerHTML = posts.slice(0, 3).map(p => {
        const cat = p.category ? p.category.name : '';
        return `
            <div class="col-xl-4 col-lg-4 col-md-6">
                <div class="single-blogs mb-30">
                    <div class="blog-img">
                        <img src="${escHtml(imgOrPlaceholder(p.cover_image_url, 'assets/img/gallery/blog1.png'))}"
                             alt="${escHtml(p.title)}" loading="lazy">
                    </div>
                    <div class="blogs-cap">
                        <div class="date-info">
                            ${cat ? `<span>${escHtml(cat)}</span>` : ''}
                            <p>${fmtDate(p.published_at || p.created_at)}</p>
                        </div>
                        <h4>${escHtml(p.title)}</h4>
                        <a href="blog_details.html?slug=${encodeURIComponent(p.slug)}" class="read-more1">Read more</a>
                    </div>
                </div>
            </div>`;
    }).join('');
}

/* ---- Blog detail render helpers ---- */

function renderBlogDetails(post) {
    const cover = document.getElementById('post-cover');
    if (cover) {
        cover.src = imgOrPlaceholder(post.cover_image_url, 'assets/img/blog/single_blog_1.png');
        cover.alt = post.title || '';
    }

    const titleEl = document.getElementById('post-title');
    if (titleEl) titleEl.textContent = post.title || '';

    const metaEl = document.getElementById('post-meta');
    if (metaEl) {
        const parts = [];
        if (post.author_name) {
            parts.push(`<li><a href="#"><i class="fa fa-user"></i> ${escHtml(post.author_name)}</a></li>`);
        }
        if (post.category) {
            parts.push(`<li><a href="blog.html?category=${encodeURIComponent(post.category.slug)}"><i class="fa fa-tag"></i> ${escHtml(post.category.name)}</a></li>`);
        }
        const date = post.published_at || post.created_at;
        if (date) {
            parts.push(`<li><a href="#"><i class="fa fa-calendar"></i> ${fmtDate(date)}</a></li>`);
        }
        if (post.read_time) {
            parts.push(`<li><a href="#"><i class="fa fa-clock-o"></i> ${post.read_time} min read</a></li>`);
        }
        metaEl.innerHTML = parts.join('');
    }

    const bodyEl = document.getElementById('post-body');
    if (bodyEl) bodyEl.innerHTML = post.content || '';

    const tagsWrap = document.getElementById('post-tags-wrap');
    const tagsEl = document.getElementById('post-tags');
    if (tagsWrap && tagsEl) {
        const tagList = post.tag_list || [];
        if (tagList.length) {
            tagsEl.innerHTML = tagList.map(t =>
                `<a href="blog.html?tag=${encodeURIComponent(t)}">${escHtml(t)}</a>`
            ).join('');
            tagsWrap.style.display = '';
        } else {
            tagsWrap.style.display = 'none';
        }
    }

    if (post.title) document.title = post.title + ' | PetCare';
}

function renderRelatedPosts(posts) {
    const section = document.getElementById('related-posts-section');
    const container = document.getElementById('related-posts');
    if (!section || !container) return;
    if (!posts || !posts.length) {
        section.style.display = 'none';
        return;
    }
    section.style.display = '';
    container.innerHTML = posts.slice(0, 3).map(p => `
        <div class="col-lg-4 col-md-6 mb-30">
            <div class="related-post-card">
                <img src="${escHtml(imgOrPlaceholder(p.cover_image_url))}" alt="${escHtml(p.title)}" loading="lazy">
                <h4><a href="blog_details.html?slug=${encodeURIComponent(p.slug)}">${escHtml(p.title)}</a></h4>
                <span class="bd-date">${fmtDate(p.published_at || p.created_at)}</span>
            </div>
        </div>`).join('');
}

function renderArticleNavigation(prev, next) {
    const navEl = document.getElementById('article-navigation');
    if (!navEl) return;
    if (!prev && !next) {
        const wrap = navEl.closest('.navigation-top');
        if (wrap) wrap.style.display = 'none';
        return;
    }

    const prevHtml = prev
        ? `<div class="col-lg-6 col-md-6 col-12 nav-left flex-row d-flex justify-content-start align-items-center">
               <div class="thumb"><a href="blog_details.html?slug=${encodeURIComponent(prev.slug)}">
                   <img class="img-fluid" src="${escHtml(imgOrPlaceholder(prev.cover_image_url, 'assets/img/post/preview.png'))}" alt="${escHtml(prev.title)}" style="width:75px;height:60px;object-fit:cover">
               </a></div>
               <div class="arrow"><a href="blog_details.html?slug=${encodeURIComponent(prev.slug)}">
                   <span class="lnr text-white ti-arrow-left"></span>
               </a></div>
               <div class="detials">
                   <p>Prev Post</p>
                   <a href="blog_details.html?slug=${encodeURIComponent(prev.slug)}"><h4>${escHtml(prev.title)}</h4></a>
               </div>
           </div>`
        : '<div class="col-lg-6 col-md-6 col-12"></div>';

    const nextHtml = next
        ? `<div class="col-lg-6 col-md-6 col-12 nav-right flex-row d-flex justify-content-end align-items-center">
               <div class="detials">
                   <p>Next Post</p>
                   <a href="blog_details.html?slug=${encodeURIComponent(next.slug)}"><h4>${escHtml(next.title)}</h4></a>
               </div>
               <div class="arrow"><a href="blog_details.html?slug=${encodeURIComponent(next.slug)}">
                   <span class="lnr text-white ti-arrow-right"></span>
               </a></div>
               <div class="thumb"><a href="blog_details.html?slug=${encodeURIComponent(next.slug)}">
                   <img class="img-fluid" src="${escHtml(imgOrPlaceholder(next.cover_image_url, 'assets/img/post/next.png'))}" alt="${escHtml(next.title)}" style="width:75px;height:60px;object-fit:cover">
               </a></div>
           </div>`
        : '<div class="col-lg-6 col-md-6 col-12"></div>';

    navEl.innerHTML = prevHtml + nextHtml;
}

/* Highlight the nav link that matches the current page */
function highlightActiveNav() {
    const page = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('#navigation > li > a').forEach(function (link) {
        const href = (link.getAttribute('href') || '').split('?')[0];
        if (href === page) link.closest('li').classList.add('active');
    });
}

/* Auto-init on every page */
document.addEventListener('DOMContentLoaded', function () {
    initAuthButtons();
    loadFooter();
    highlightActiveNav();
});
