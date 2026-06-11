import pathlib

def w(path, content):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.lstrip('\n'), encoding='utf-8')
    print(f'  {path}')

w('templates/base.html', '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ site.title }}{% endblock %}</title>
    <meta name="description" content="{% block meta_desc %}{{ site.subtitle }}{% endblock %}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;800&family=Crimson+Pro:wght@300;400;500;600&family=JetBrains+Mono:wght@300;400&display=swap" rel="stylesheet">
    <style>
        :root{--bg:#06060a;--surface:#0e0e14;--card:#14141c;--card-hover:#1a1a24;--border:#1e1e2a;--border-light:#2a2a38;--accent:#c9a84c;--accent-dim:#8a7230;--accent-glow:rgba(201,168,76,0.08);--text:#e4e0d8;--text-secondary:#a09888;--text-muted:#605850;--text-faint:#3a3530;--tag-bg:rgba(201,168,76,0.1);--tag-border:rgba(201,168,76,0.2);--radius:6px;--radius-lg:12px;--font-display:'Playfair Display',Georgia,serif;--font-body:'Crimson Pro','Noto Serif TC',serif;--font-mono:'JetBrains Mono',monospace;--max-width:1200px;--header-height:72px}
        *{margin:0;padding:0;box-sizing:border-box}
        html{scroll-behavior:smooth;-webkit-font-smoothing:antialiased}
        body{font-family:var(--font-body);font-size:17px;line-height:1.7;color:var(--text);background:var(--bg);min-height:100vh}
        body::before{content:'';position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse 800px 600px at 15% 20%,rgba(201,168,76,0.03) 0%,transparent 70%25),radial-gradient(ellipse 600px 400px at 85% 80%25,rgba(100,80,180,0.02) 0%,transparent 70%25)}
        body::after{content:'';position:fixed;inset:0;opacity:0.025;pointer-events:none;z-index:0;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
        .page-wrapper{position:relative;z-index:1}
        header{position:sticky;top:0;z-index:100;height:var(--header-height);display:flex;align-items:center;justify-content:space-between;padding:0 clamp(20px,4vw,48px);background:rgba(6,6,10,0.85);backdrop-filter:blur(20px);border-bottom:1px solid var(--border)}
        .logo{font-family:var(--font-display);font-size:1.35rem;font-weight:700;color:var(--text);text-decoration:none;letter-spacing:-0.02em}
        .logo span{color:var(--accent)}
        nav{display:flex;align-items:center;gap:8px}
        nav a{font-family:var(--font-mono);font-size:0.72rem;color:var(--text-muted);text-decoration:none;padding:6px 14px;border-radius:100px;transition:all 0.25s ease;letter-spacing:0.04em;text-transform:uppercase}
        nav a:hover{color:var(--accent);background:var(--accent-glow)}
        .hero{padding:clamp(60px,10vh,120px) clamp(20px,4vw,48px) clamp(40px,6vh,80px);max-width:var(--max-width);margin:0 auto}
        .hero-label{font-family:var(--font-mono);font-size:0.7rem;font-weight:300;color:var(--accent);text-transform:uppercase;letter-spacing:0.2em;margin-bottom:20px;opacity:0;animation:fadeUp 0.6s ease forwards}
        .hero h1{font-family:var(--font-display);font-size:clamp(2.4rem,5vw,4rem);font-weight:800;line-height:1.1;color:var(--text);letter-spacing:-0.03em;max-width:700px;opacity:0;animation:fadeUp 0.6s ease 0.1s forwards}
        .hero h1 em{font-style:italic;color:var(--accent)}
        .hero-sub{margin-top:20px;font-size:1.1rem;font-weight:300;color:var(--text-secondary);max-width:550px;opacity:0;animation:fadeUp 0.6s ease 0.2s forwards}
        .hero-meta{margin-top:32px;display:flex;gap:32px;opacity:0;animation:fadeUp 0.6s ease 0.3s forwards}
        .hero-stat{font-family:var(--font-mono);font-size:0.75rem;color:var(--text-muted)}
        .hero-stat strong{color:var(--accent);font-weight:400}
        .filter-bar{max-width:var(--max-width);margin:0 auto;padding:0 clamp(20px,4vw,48px) 32px;display:flex;flex-wrap:wrap;gap:8px;opacity:0;animation:fadeUp 0.6s ease 0.35s forwards}
        .filter-btn{font-family:var(--font-mono);font-size:0.68rem;padding:5px 14px;border:1px solid var(--border);border-radius:100px;background:transparent;color:var(--text-muted);cursor:pointer;transition:all 0.2s ease}
        .filter-btn:hover,.filter-btn.active{border-color:var(--accent);color:var(--accent);background:var(--accent-glow)}
        .divider{max-width:var(--max-width);margin:0 auto;padding:0 clamp(20px,4vw,48px)}
        .divider hr{border:none;height:1px;background:var(--border)}
        .articles-grid{max-width:var(--max-width);margin:0 auto;padding:32px clamp(20px,4vw,48px) 60px;display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:20px}
        .article-card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius-lg);padding:28px;text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:14px;transition:all 0.35s cubic-bezier(0.23,1,0.32,1);position:relative;overflow:hidden;opacity:0;animation:fadeUp 0.5s ease forwards}
        .article-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--accent-dim),var(--accent),var(--accent-dim));opacity:0;transition:opacity 0.35s ease}
        .article-card:hover{border-color:var(--border-light);background:var(--card-hover);transform:translateY(-4px);box-shadow:0 20px 60px rgba(0,0,0,0.3)}
        .article-card:hover::before{opacity:1}
        .article-card:nth-child(1){animation-delay:0.05s}.article-card:nth-child(2){animation-delay:0.1s}.article-card:nth-child(3){animation-delay:0.15s}.article-card:nth-child(4){animation-delay:0.2s}.article-card:nth-child(5){animation-delay:0.25s}.article-card:nth-child(6){animation-delay:0.3s}
        .card-meta{display:flex;align-items:center;justify-content:space-between;gap:12px}
        .card-tags{display:flex;gap:6px;flex-wrap:wrap}
        .card-tag{font-family:var(--font-mono);font-size:0.62rem;padding:3px 10px;border-radius:100px;background:var(--tag-bg);border:1px solid var(--tag-border);color:var(--accent)}
        .card-date{font-family:var(--font-mono);font-size:0.65rem;color:var(--text-faint);white-space:nowrap}
        .card-title{font-family:var(--font-display);font-size:1.25rem;font-weight:600;line-height:1.35;color:var(--text)}
        .card-summary{font-size:0.95rem;font-weight:300;color:var(--text-secondary);line-height:1.65;flex:1}
        .card-source{font-family:var(--font-mono);font-size:0.65rem;color:var(--text-faint);display:flex;align-items:center;gap:6px}
        .card-source::before{content:'';width:4px;height:4px;border-radius:50%25;background:var(--accent-dim)}
        .empty-state{grid-column:1/-1;text-align:center;padding:80px 20px;color:var(--text-muted);font-family:var(--font-display);font-size:1.3rem}
        footer{max-width:var(--max-width);margin:0 auto;padding:40px clamp(20px,4vw,48px) 60px;border-top:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px}
        .footer-left{font-family:var(--font-mono);font-size:0.7rem;color:var(--text-faint)}
        .footer-right{font-family:var(--font-mono);font-size:0.65rem;color:var(--text-faint)}
        .footer-right a{color:var(--accent-dim);text-decoration:none}
        .footer-right a:hover{color:var(--accent)}
        @keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
        .article-header{max-width:780px;margin:0 auto;padding:clamp(40px,8vh,100px) clamp(20px,4vw,48px) 40px}
        .article-back{font-family:var(--font-mono);font-size:0.72rem;color:var(--text-muted);text-decoration:none;display:inline-flex;align-items:center;gap:8px;margin-bottom:40px;transition:color 0.2s}
        .article-back:hover{color:var(--accent)}
        .article-header .card-tags{margin-bottom:16px}
        .article-header h1{font-family:var(--font-display);font-size:clamp(1.8rem,4vw,2.8rem);font-weight:800;line-height:1.2;color:var(--text);opacity:0;animation:fadeUp 0.6s ease 0.1s forwards}
        .article-meta-bar{margin-top:24px;display:flex;flex-wrap:wrap;gap:20px;font-family:var(--font-mono);font-size:0.7rem;color:var(--text-muted);opacity:0;animation:fadeUp 0.6s ease 0.2s forwards}
        .article-body{max-width:780px;margin:0 auto;padding:20px clamp(20px,4vw,48px) 80px;opacity:0;animation:fadeUp 0.6s ease 0.3s forwards}
        .article-body h2{font-family:var(--font-display);font-size:1.6rem;font-weight:600;margin:48px 0 16px;color:var(--text)}
        .article-body h3{font-family:var(--font-display);font-size:1.25rem;font-weight:600;margin:36px 0 12px;color:var(--text)}
        .article-body p{margin-bottom:20px;color:var(--text-secondary);font-weight:300;font-size:1.05rem}
        .article-body strong{color:var(--text);font-weight:500}
        .article-body ul,.article-body ol{margin:0 0 20px 24px;color:var(--text-secondary)}
        .article-body li{margin-bottom:8px;font-weight:300}
        .article-body blockquote{border-left:3px solid var(--accent-dim);padding:12px 24px;margin:24px 0;background:var(--accent-glow);border-radius:0 var(--radius) var(--radius) 0}
        .article-body blockquote p{color:var(--text);font-style:italic;margin-bottom:0}
        .article-body code{font-family:var(--font-mono);font-size:0.85em;background:var(--surface);padding:2px 8px;border-radius:4px;color:var(--accent)}
        .article-body pre{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px;overflow-x:auto;margin:24px 0}
        .article-body pre code{background:none;padding:0;font-size:0.82rem;color:var(--text-secondary)}
        .original-link{margin-top:48px;padding:20px 24px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg);font-family:var(--font-mono);font-size:0.78rem}
        .original-link a{color:var(--accent);text-decoration:none}
        .original-link a:hover{text-decoration:underline}
        @media(max-width:768px){.articles-grid{grid-template-columns:1fr}.hero-meta{flex-direction:column;gap:8px}footer{flex-direction:column;text-align:center}}
    </style>
    {% block head_extra %}{% endblock %}
</head>
<body>
    <div class="page-wrapper">
        <header>
            <a href="{{ '/' if site.url else './' }}" class="logo"><span>&#9670;</span> {{ site.title }}</a>
            <nav>
                <a href="{{ '/' if site.url else './' }}">首頁</a>
                <a href="{{ '/rss.xml' if site.url else './rss.xml' }}">RSS</a>
            </nav>
        </header>
        {% block content %}{% endblock %}
        <footer>
            <div class="footer-left">{{ site.title }}  {{ site.subtitle }}</div>
            <div class="footer-right">由 AI 自動生成 &middot; <a href="https://github.com" target="_blank">GitHub Pages</a></div>
        </footer>
    </div>
    {% block scripts %}{% endblock %}
</body>
</html>''')

w('templates/index.html', '''{% extends "base.html" %}
{% block content %}
<section class="hero">
    <div class="hero-label">Auto-curated by AI &middot; Updated Daily</div>
    <h1>追蹤每一個<br><em>改變世界</em>的 AI 瞬間</h1>
    <p class="hero-sub">{{ site.subtitle }}  由 AI 自動抓取、改寫、分類，每日為你精選最有價值的 AI 資訊。</p>
    <div class="hero-meta">
        <div class="hero-stat"><strong>{{ articles | length }}</strong> 篇文章</div>
        <div class="hero-stat"><strong>{{ all_tags | length }}</strong> 個主題</div>
        <div class="hero-stat">Powered by <strong>AI</strong></div>
    </div>
</section>
{% if all_tags %}
<div class="filter-bar">
    <button class="filter-btn active" onclick="filterArticles('all')">全部</button>
    {% for tag in all_tags %}
    <button class="filter-btn" onclick="filterArticles('{{ tag }}')">{{ tag }}</button>
    {% endfor %}
</div>
{% endif %}
<div class="divider"><hr></div>
<div class="articles-grid" id="articles-grid">
    {% for article in articles %}
    <a href="{{ '/article/' + article.id + '/' if site.url else './article/' + article.id + '/' }}" class="article-card" data-tags="{{ article.tags | join(',') }}">
        <div class="card-meta">
            <div class="card-tags">{% for tag in article.tags[:2] %}<span class="card-tag">{{ tag }}</span>{% endfor %}</div>
            <span class="card-date">{{ article.scraped_at | time_ago if article.scraped_at else '' }}</span>
        </div>
        <h2 class="card-title">{{ article.title }}</h2>
        <p class="card-summary">{{ article.summary }}</p>
        <span class="card-source">{{ article.original_source }}</span>
    </a>
    {% else %}
    <div class="empty-state">還沒有文章  等待 AI 抓取和處理中...</div>
    {% endfor %}
</div>
{% endblock %}
{% block scripts %}
<script>
function filterArticles(tag){
    document.querySelectorAll('.article-card').forEach(c=>{c.style.display=(tag==='all')?'':((c.dataset.tags||'').includes(tag)?'':'none')});
    document.querySelectorAll('.filter-btn').forEach(b=>{b.classList.toggle('active',b.textContent.trim()===(tag==='all'?'全部':tag))});
}
</script>
{% endblock %}''')

w('templates/article.html', '''{% extends "base.html" %}
{% block title %}{{ article.title }}  {{ site.title }}{% endblock %}
{% block meta_desc %}{{ article.meta_description or article.summary }}{% endblock %}
{% block content %}
<article>
    <div class="article-header">
        <a href="{{ '/' if site.url else '../' }}" class="article-back">&larr; 返回首頁</a>
        <div class="card-tags">{% for tag in article.tags %}<span class="card-tag">{{ tag }}</span>{% endfor %}</div>
        <h1>{{ article.title }}</h1>
        <div class="article-meta-bar">
            <span>{{ article.original_source }}</span>
            <span>{{ article.scraped_at | format_date }}</span>
            <span>分類：{{ article.category }}</span>
        </div>
    </div>
    <div class="article-body">
        {{ article.content | md_to_html | safe }}
        <div class="original-link">原始來源：<a href="{{ article.original_url }}" target="_blank" rel="noopener">{{ article.original_title }}</a></div>
    </div>
</article>
{% endblock %}''')

print('模板建立完成！')
