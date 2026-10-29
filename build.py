"""Gera a prévia do site Sunpeak: index.html + lojas/<slug>.html.

Dados de LOJAS tirados do site oficial e dos perfis do Instagram em 29/10/2026.
Campo None = ainda não confirmado com a Sunpeak; aparece no site marcado como "a confirmar".
Rodar: python build.py
"""
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent
DOMINIO = "https://sunpeak.com.br"
PREVIA = True  # True = faixa "prévia" + noindex. Trocar pra False quando for pro domínio real.

LOJAS = [
    dict(slug="center-vale", cidade="São José dos Campos", filtro="sjc", nome="Center Vale Shopping",
         matriz=True, endereco=None, cep=None, tel="(12) 3941-9004", wa="12997880909",
         ig="sunpeak_centervale", horario=None, marcas=None,
         sobre="A matriz da rede. Foi daqui que a Sunpeak cresceu para as outras cidades do Vale."),
    dict(slug="vale-sul", cidade="São José dos Campos", filtro="sjc", nome="Vale Sul Shopping",
         endereco=None, cep=None, tel="(12) 3931-7615", wa="12997470606",
         ig="sunpeak_valesul", horario=None, marcas=None,
         sobre="Palco do lançamento da collab Quiksilver x Sunpeak, em 11 de setembro de 2026, com brinde, som e coquetel para os clientes.",
         fotos=[("collab-lancamento.jpg", "Arte do evento de lançamento Quiksilver x Sunpeak no Vale Sul Shopping", "O lançamento da collab foi aqui")]),
    dict(slug="centro", cidade="São José dos Campos", filtro="sjc", nome="Centro",
         endereco="Rua Coronel José Monteiro, 233, Centro", cep="12210-140", tel="(12) 3921-2209",
         wa="12997942626", ig="sunpeak_centro", horario=None, marcas=None,
         sobre="A loja de rua da Sunpeak, no coração do centro de São José dos Campos."),
    dict(slug="oriente", cidade="São José dos Campos", filtro="sjc", nome="Shopping Oriente",
         endereco=None, cep=None, tel=None, wa="12997334242",
         ig="sunpeak_jdoriente", horario=None, marcas=None, sobre=None),
    dict(slug="taubate", cidade="Taubaté", filtro="taubate", nome="Taubaté Shopping",
         endereco="Av. Charles Schnneider, 1700, lojas 58/59", cep=None, tel="(12) 3633-8871",
         wa="12997102727", ig="sunpeak_taubate", horario=None,
         marcas=["Vans", "Oakley", "Rip Curl", "New Era", "Converse", "G-Shock", "Evoke", "Quiksilver", "Öus"],
         sobre="A Sunpeak de Taubaté, com as marcas de surf e skate que você acompanha no nosso Instagram.",
         fotos=[("taubate-loja.jpg", "Interior da Sunpeak Taubaté Shopping com a parede de tênis", "Dentro da loja"),
                ("taubate-equipe.jpg", "Vendedora da Sunpeak Taubaté entre as araras de moletom", "Nossa equipe")]),
    dict(slug="guaratingueta", cidade="Guaratinguetá", filtro="guara", nome="Buriti Shopping Guará",
         endereco=None, cep=None, tel="(12) 3122-0620", wa="12997970505",
         ig="sunpeakguara", horario=None, marcas=None, sobre=None),
]
MARCAS_REDE = ["Vans", "Oakley", "Rip Curl", "Converse", "Quiksilver", "Volcom", "Hurley", "Öus", "Hang Loose"]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">')

ICONS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
<symbol id="i-wa" viewBox="0 0 24 24"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.6.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48 0 1.46 1.07 2.88 1.21 3.08.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.69.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2.01-1.41.25-.7.25-1.29.17-1.41-.07-.13-.27-.2-.57-.35zM12.04 21.5h-.01a9.4 9.4 0 0 1-4.8-1.31l-.34-.2-3.57.94.95-3.48-.22-.36a9.38 9.38 0 0 1-1.44-5.01c0-5.2 4.23-9.43 9.44-9.43 2.52 0 4.89.98 6.67 2.77a9.37 9.37 0 0 1 2.76 6.67c0 5.2-4.24 9.43-9.44 9.43zm8.03-17.46A11.27 11.27 0 0 0 12.04.72C5.79.72.7 5.8.7 12.06c0 2 .52 3.95 1.52 5.67L.6 23.28l5.68-1.49a11.3 11.3 0 0 0 5.75 1.47h.01c6.25 0 11.34-5.09 11.34-11.34 0-3.03-1.18-5.88-3.32-8.02z"/></symbol>
<symbol id="i-phone" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></g></symbol>
</svg>"""


def svg(i):
    return f'<svg viewBox="0 0 24 24" fill="currentColor"><use href="#{i}"/></svg>'


def todo(txt="a confirmar"):
    return f'<span class="todo">{txt}</span>'


def foto(arq, alt, legenda, base="", cls="shot"):
    return (f'<figure class="{cls}"><img src="{base}img/fotos/{arq}" alt="{alt}" loading="lazy">'
            f'<figcaption>{legenda}</figcaption></figure>')


def fotos_loja(l):
    fs = [foto(a, alt, leg, "../") for a, alt, leg in (l.get("fotos") or [])]
    vazios = [f"Foto da fachada<br>({l['nome']})", "Foto da equipe<br>da loja"][len(fs):]
    return "\n        ".join(fs + [f'<div class="photo-slot">{t}</div>' for t in vazios])


def fmt_wa(n):
    return f"({n[:2]}) {n[2:7]}-{n[7:]}"


def wa_link(l):
    msg = f"Oi! Vim pelo site da Sunpeak (loja {l['nome']}). Queria saber se vocês têm..."
    return f"https://wa.me/55{l['wa']}?text={quote(msg)}"


def tel_link(t):
    return "tel:+55" + "".join(c for c in t if c.isdigit())


def busca_maps(l):
    return f"Sunpeak Surf {l['endereco'] or l['nome']} {l['cidade']}"


def map_link(l):
    return "https://www.google.com/maps/search/?api=1&query=" + quote(busca_maps(l))


def map_embed(l):
    return "https://www.google.com/maps?output=embed&q=" + quote(busca_maps(l))


def titulo(l):
    return f"Sunpeak {l['nome']}" if l["nome"] != "Centro" else "Sunpeak Centro"


def head(title, desc, canonical, css):
    robots = '<meta name="robots" content="noindex, nofollow">' if PREVIA else ""
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{robots}
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
{FONTS}
<link rel="stylesheet" href="{css}">
</head>
<body>
{'<div class="preview">Prévia de proposta · Solução Digital 4.0 · não é o site oficial</div>' if PREVIA else ''}"""


def header(base, wa_btn):
    return f"""<header>
  <div class="wrap nav">
    <a href="{base}index.html"><img src="{base}img/logo.png" alt="Sunpeak Surf" width="121" height="40"></a>
    <ul>
      <li><a href="{base}index.html#lojas">Lojas</a></li>
      <li><a href="{base}index.html#collab">Quiksilver x Sunpeak</a></li>
      <li><a href="{base}index.html#cena">Na cena</a></li>
      <li><a href="{base}index.html#historia">História</a></li>
    </ul>
    {wa_btn}
  </div>
</header>"""


def footer(base):
    links = "".join(f'<li><a href="{base}lojas/{l["slug"]}.html">{titulo(l)}</a></li>' for l in LOJAS)
    igs = "".join(f'<li><a href="https://instagram.com/{l["ig"]}" target="_blank" rel="noopener">@{l["ig"]}</a></li>' for l in LOJAS)
    return f"""<footer>
  <div class="wrap foot">
    <div>
      <img src="{base}img/logo.png" alt="Sunpeak Surf" width="115" height="38">
      <div>Sunpeak Surf · desde 1992<br>Surf · Cultura · Amizade · Lifestyle<br><br>Rita Narikawa EPP · CNPJ 03.284.807/0001-91</div>
    </div>
    <div><strong>Lojas</strong><ul>{links}</ul></div>
    <div><strong>Instagram</strong><ul><li><a href="https://instagram.com/sunpeakoficial" target="_blank" rel="noopener">@sunpeakoficial</a></li>{igs}</ul></div>
  </div>
</footer>"""


SHEET = """<div class="sheet-bg" id="sheet" role="dialog" aria-modal="true" aria-labelledby="sheet-t">
  <div class="sheet">
    <button class="close" aria-label="Fechar">&times;</button>
    <h3 id="sheet-t">Qual loja fica mais perto?</h3>
    <p>Você vai direto pro WhatsApp da loja escolhida.</p>
    {itens}
  </div>
</div>"""

SCRIPT_HOME = """<script>
document.querySelectorAll(".filters button").forEach(b => b.addEventListener("click", () => {
  document.querySelectorAll(".filters button").forEach(x => x.classList.toggle("on", x === b));
  document.querySelectorAll(".store").forEach(s => s.hidden = b.dataset.city !== "todas" && s.dataset.city !== b.dataset.city);
}));
const sheet = document.getElementById("sheet");
document.querySelectorAll("[data-open-sheet]").forEach(b => b.addEventListener("click", () => sheet.classList.add("open")));
sheet.addEventListener("click", e => { if (e.target === sheet || e.target.classList.contains("close")) sheet.classList.remove("open"); });
document.addEventListener("keydown", e => { if (e.key === "Escape") sheet.classList.remove("open"); });
</script>"""


def card_loja(l):
    info = []
    if l["endereco"]:
        info.append(f"<span>{l['endereco']}</span>")
    info.append(f"<span>WhatsApp {fmt_wa(l['wa'])}</span>")
    if l["tel"]:
        info.append(f"<span>Fixo {l['tel']}</span>")
    badge = '<span class="badge">MATRIZ</span>' if l.get("matriz") else ""
    return f"""<article class="store" data-city="{l['filtro']}">
  <div><div class="city">{l['cidade']}</div><h3><a href="lojas/{l['slug']}.html">{l['nome']}</a>{badge}</h3></div>
  <div class="info">{''.join(info)}</div>
  <div class="actions">
    <a class="btn btn-wa" href="{wa_link(l)}" target="_blank" rel="noopener">{svg('i-wa')}WhatsApp</a>
    <a class="btn btn-line" href="lojas/{l['slug']}.html">Ver a loja</a>
  </div>
</article>"""


def pagina_home():
    marcas = "".join(f"<span>{m.upper()}</span>" for m in MARCAS_REDE)
    cards = "\n".join(card_loja(l) for l in LOJAS)
    itens = "".join(f'<a href="{wa_link(l)}" target="_blank" rel="noopener"><span>{l["nome"]}<small>{l["cidade"]}</small></span>{svg("i-wa")}</a>' for l in LOJAS)
    wa_btn = f'<button class="btn btn-wa" data-open-sheet>{svg("i-wa")}<span>Falar no WhatsApp</span></button>'
    org = {
        "@context": "https://schema.org", "@type": "Organization", "name": "Sunpeak Surf",
        "url": DOMINIO, "logo": f"{DOMINIO}/img/logo.png", "foundingDate": "1992",
        "sameAs": ["https://instagram.com/sunpeakoficial"] + [f"https://instagram.com/{l['ig']}" for l in LOJAS],
        "department": [{"@type": "ClothingStore", "name": titulo(l), "url": f"{DOMINIO}/lojas/{l['slug']}"} for l in LOJAS],
    }
    return f"""{head("Sunpeak Surf | Surf shop do Vale do Paraíba desde 1992",
          "Sunpeak Surf, surf shop do Vale do Paraíba desde 1992. 6 lojas em São José dos Campos, Taubaté e Guaratinguetá. Vans, Oakley, Rip Curl, Converse, Quiksilver e mais.",
          DOMINIO + "/", "assets/site.css")}
{header("", wa_btn)}
<main id="topo">
  <section class="hero">
    <div class="sun"></div>
    <div class="wrap hero-grid">
     <div>
      <div class="motto">Surf <i>·</i> Cultura <i>·</i> Amizade <i>·</i> Lifestyle</div>
      <h1>O surf shop do Vale <em>desde 1992.</em></h1>
      <p class="lead">Vans, Oakley, Rip Curl, Converse e as marcas que fazem parte da nossa história, em 6 lojas no Vale do Paraíba. Chama a loja mais perto no WhatsApp: a gente confere tamanho, cor e separa pra você.</p>
      <div class="ctas">
        <button class="btn btn-wa" data-open-sheet>{svg('i-wa')}Chamar a loja mais perto</button>
        <a class="btn btn-ghost" href="#lojas">Ver as 6 lojas</a>
      </div>
      <div class="stats">
        <div><b>30+</b><span>anos de surf e skate</span></div>
        <div><b>6</b><span>lojas no Vale</span></div>
        <div><b>3</b><span>cidades</span></div>
      </div>
     </div>
     <div class="hero-photos">
       <img class="p1" src="img/fotos/collab-camiseta.jpg" alt="Rapaz de costas com a camiseta da collab Quiksilver x Sunpeak, entre palmeiras">
       <img class="p2" src="img/fotos/tenis-ous.jpg" alt="Tênis Öus azul-marinho com detalhes caramelo">
     </div>
    </div>
    <svg class="waves" viewBox="0 0 1440 120" preserveAspectRatio="none"><path fill="#fbf7f1" d="M0,64 C180,110 360,20 540,48 C720,76 900,118 1080,86 C1260,54 1350,30 1440,40 L1440,120 L0,120 Z"/></svg>
  </section>

  <div class="brands"><div class="wrap"><p>Revendedor autorizado</p><div class="brand-row">{marcas}</div></div></div>

  <section class="block" id="lojas">
    <div class="wrap">
      <span class="kicker">Nossas lojas</span>
      <h2>Escolha a sua Sunpeak</h2>
      <p class="sub">Cada loja tem o próprio WhatsApp e a própria equipe. Chama a mais perto, pede foto do produto e separa antes de sair de casa.</p>
      <div class="filters">
        <button class="on" data-city="todas">Todas</button>
        <button data-city="sjc">São José dos Campos</button>
        <button data-city="taubate">Taubaté</button>
        <button data-city="guara">Guaratinguetá</button>
      </div>
      <div class="stores">
{cards}
      </div>
    </div>
  </section>

  <section class="block collab" id="collab">
    <div class="wrap collab-grid">
      <div>
        <div class="collab-mark">QUIKSILVER <span>×</span> SUNPEAK</div>
        <h2 style="margin-top:18px">Algumas marcas fazem parte da nossa história</h2>
        <p>A Quiksilver é uma delas. Anos dividindo a mesma paixão pelo surf, pela cultura e por esse estilo de vida viraram uma coleção nossa: camisetas da collab Quiksilver x Sunpeak.</p>
        <div class="facts"><span>Collab oficial</span><span>Lançada em 11/09/2026</span><span>Vale Sul Shopping</span></div>
        <div class="ctas"><button class="btn btn-or" data-open-sheet>Perguntar se tem na minha loja</button></div>
      </div>
      {foto('collab-camisetas-pedra.jpg', 'Três camisetas da collab Quiksilver x Sunpeak sobre pedras na praia', 'As camisetas da collab')}
    </div>
  </section>

  <section class="block" id="cena">
    <div class="wrap">
      <span class="kicker">Na cena do Vale</span>
      <h2>A gente não só vende. A gente anda junto.</h2>
      <p class="sub">Campeonato, lançamento, som na loja: a Sunpeak está onde o surf e o skate do Vale acontecem.</p>
      <div class="scene">
        <div class="card"><img class="card-img" src="img/fotos/vale-radness.jpg" alt="Pôster do circuito Vale Radness com patrocínio Sunpeak" loading="lazy"><div class="n">Skate</div><h3>Vale Radness</h3><p>Patrocinadora do circuito paulista de bowl e park em São José dos Campos, com categorias do mirim ao amador.</p></div>
        <div class="card"><img class="card-img" src="img/fotos/collab-lancamento.jpg" alt="Arte do evento de lançamento Quiksilver x Sunpeak" loading="lazy"><div class="n">Lançamentos</div><h3>Evento na loja</h3><p>Lançamento de coleção vira encontro: brinde, preço especial e coquetel pra quem é cliente. Você é nosso convidado.</p></div>
        <div class="card"><img class="card-img" src="img/fotos/lifestyle-volcom.jpg" alt="Moça com camiseta listrada Volcom e óculos escuros" loading="lazy"><div class="n">Drops e edições limitadas</div><h3>Chega primeiro aqui</h3><p>Novidades das marcas e edições numeradas, como Evoke x Street Fighter, chegam nas nossas lojas. Segue a sua loja no Instagram pra não perder.</p></div>
      </div>
    </div>
  </section>

  <section class="block voices">
    <div class="wrap">
      <span class="kicker">Quem compra fala</span>
      <h2>Comentários de clientes no nosso Instagram</h2>
      <div class="quotes">
        <div class="quote"><p>Melhor loja surfwear</p><small>Cliente, no Instagram @sunpeakoficial</small></div>
        <div class="quote"><p>A melhor do vale</p><small>Cliente, no Instagram @sunpeakoficial</small></div>
        <div class="quote"><p>Parceria de sucesso!</p><small>Cliente, sobre a collab com a Quiksilver</small></div>
      </div>
    </div>
  </section>

  <section class="block" id="historia">
    <div class="wrap story">
      <div>
        <span class="kicker">Nossa história</span>
        <h2>Começou com uma loja em São José</h2>
        <p>A primeira Sunpeak abriu em 1992, em São José dos Campos. Mais de três décadas depois, são 6 lojas no Vale e o mesmo jeito: muito mais que produto, estilo e conteúdo original do mundo do surf e do skate.</p>
        <p>Muita coisa mudou desde então. A paixão pelo surf, pela cultura e pelas amizades que nascem no balcão continua a mesma.</p>
      </div>
      {foto('taubate-equipe.jpg', 'Vendedora da Sunpeak entre as araras de moletom', 'Equipe Sunpeak, Taubaté Shopping')}
    </div>
  </section>

  <div class="final">
    <h2>Viu algo no Instagram?</h2>
    <p>Manda o print pra loja mais perto e a gente confere tamanho e cor pra você.</p>
    <button class="btn btn-wa" data-open-sheet>{svg('i-wa')}Chamar no WhatsApp</button>
  </div>
</main>
{footer("")}
<button class="fab" data-open-sheet aria-label="Falar no WhatsApp">{svg('i-wa')}</button>
{SHEET.format(itens=itens)}
{ICONS}
<script type="application/ld+json">{json.dumps(org, ensure_ascii=False)}</script>
{SCRIPT_HOME}
</body>
</html>
"""


def schema_loja(l):
    addr = {"@type": "PostalAddress", "addressLocality": l["cidade"], "addressRegion": "SP", "addressCountry": "BR"}
    if l["endereco"]:
        addr["streetAddress"] = l["endereco"]
    if l["cep"]:
        addr["postalCode"] = l["cep"]
    d = {
        "@context": "https://schema.org", "@type": "ClothingStore", "name": titulo(l),
        "url": f"{DOMINIO}/lojas/{l['slug']}", "image": f"{DOMINIO}/img/logo.png",
        "telephone": "+55 " + (l["tel"] or fmt_wa(l["wa"])), "address": addr,
        "parentOrganization": {"@type": "Organization", "name": "Sunpeak Surf", "url": DOMINIO},
        "sameAs": [f"https://instagram.com/{l['ig']}"],
        "brand": [{"@type": "Brand", "name": m} for m in (l["marcas"] or MARCAS_REDE)],
    }
    # horário (openingHoursSpecification) entra quando a Sunpeak confirmar
    return json.dumps(d, ensure_ascii=False)


def pagina_loja(l):
    t = titulo(l)
    end_txt = f"{l['endereco']}, {l['cidade']}/SP" if l["endereco"] else f"{l['nome']}, {l['cidade']}/SP"
    end_dd = (l["endereco"] + (f", CEP {l['cep']}" if l["cep"] else "") + f"<br>{l['cidade']}/SP") if l["endereco"] \
        else f"{l['nome']}, {l['cidade']}/SP<br>Loja nº {todo()}"
    tel_dd = f'<a href="{tel_link(l["tel"])}">{l["tel"]}</a>' if l["tel"] else todo()
    marcas = l["marcas"] or MARCAS_REDE
    marcas_nota = "" if l["marcas"] else f'<p style="margin-top:12px;font-size:.85rem;color:var(--muted)">Mix desta loja {todo()}</p>'
    sobre = l["sobre"] or f"Texto desta loja {todo()}: o que ela tem de diferente, quem atende, o que o cliente encontra lá."
    outras = "".join(f'<a href="{o["slug"]}.html"><small>{o["cidade"]}</small>{o["nome"]}</a>' for o in LOJAS if o is not l)
    wa_btn = f'<a class="btn btn-wa" href="{wa_link(l)}" target="_blank" rel="noopener">{svg("i-wa")}<span>WhatsApp da loja</span></a>'
    tel_btn = f'<a class="btn btn-ghost" href="{tel_link(l["tel"])}">{svg("i-phone")}Ligar</a>' if l["tel"] else ""
    desc = f"{t}: surf shop em {l['cidade']}. WhatsApp {fmt_wa(l['wa'])}. Vans, Oakley, Rip Curl, Converse e mais. Sunpeak desde 1992."
    return f"""{head(f"{t} | Surf shop em {l['cidade']}", desc, f"{DOMINIO}/lojas/{l['slug']}", "../assets/site.css")}
{header("../", wa_btn)}
<main>
  <section class="hero store-hero">
    <div class="sun"></div>
    <div class="wrap">
      <nav class="crumbs"><a href="../index.html">Início</a> › <a href="../index.html#lojas">Lojas</a> › {l['nome']}</nav>
      <div class="motto">{l['cidade']}{' <i>·</i> Matriz' if l.get('matriz') else ''}</div>
      <h1>{t}</h1>
      <p class="addr">{end_txt}</p>
      <div class="ctas" style="display:flex;flex-wrap:wrap;gap:12px;margin-top:28px">
        <a class="btn btn-wa" href="{wa_link(l)}" target="_blank" rel="noopener">{svg('i-wa')}Chamar no WhatsApp</a>
        {tel_btn}
        <a class="btn btn-ghost" href="{map_link(l)}" target="_blank" rel="noopener">{svg('i-pin')}Como chegar</a>
      </div>
    </div>
    <svg class="waves" viewBox="0 0 1440 120" preserveAspectRatio="none"><path fill="#fbf7f1" d="M0,64 C180,110 360,20 540,48 C720,76 900,118 1080,86 C1260,54 1350,30 1440,40 L1440,120 L0,120 Z"/></svg>
  </section>

  <section class="block" style="padding-top:20px">
    <div class="wrap">
      <div class="store-main">
        <div class="panel">
          <h2>Informações da loja</h2>
          <dl>
            <dt>Endereço</dt><dd>{end_dd}</dd>
            <dt>WhatsApp</dt><dd><a href="{wa_link(l)}" target="_blank" rel="noopener">{fmt_wa(l['wa'])}</a></dd>
            <dt>Telefone</dt><dd>{tel_dd}</dd>
            <dt>Horário</dt><dd>{todo()}</dd>
            <dt>Instagram</dt><dd><a href="https://instagram.com/{l['ig']}" target="_blank" rel="noopener">@{l['ig']}</a></dd>
          </dl>
        </div>
        <div class="map"><iframe src="{map_embed(l)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa da {t}"></iframe></div>
      </div>

      <div class="about">
        <div class="panel">
          <span class="kicker">Sobre esta loja</span>
          <p>{sobre}</p>
          <div class="chips">{''.join(f'<span>{m}</span>' for m in marcas)}</div>
          {marcas_nota}
        </div>
        {fotos_loja(l)}
      </div>

      <div style="margin-top:56px">
        <span class="kicker">Outras lojas Sunpeak</span>
        <div class="others">{outras}</div>
      </div>
    </div>
  </section>
</main>
{footer("../")}
<a class="fab" href="{wa_link(l)}" target="_blank" rel="noopener" aria-label="WhatsApp da {t}">{svg('i-wa')}</a>
{ICONS}
<script type="application/ld+json">{schema_loja(l)}</script>
</body>
</html>
"""


def sitemap():
    urls = [DOMINIO + "/"] + [f"{DOMINIO}/lojas/{l['slug']}" for l in LOJAS]
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
        "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n"


if __name__ == "__main__":
    (ROOT / "lojas").mkdir(exist_ok=True)
    (ROOT / "index.html").write_text(pagina_home(), encoding="utf-8")
    for l in LOJAS:
        (ROOT / "lojas" / f"{l['slug']}.html").write_text(pagina_loja(l), encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    print("ok:", 1 + len(LOJAS), "páginas")
