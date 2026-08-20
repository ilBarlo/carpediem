# CarpeDiem — Sito Web Bottega Ceramiche

## Cliente
Bottega di ceramiche artigianali a Grottaglie (TA), storico centro pugliese della ceramica.

## Obiettivo
Sito web completo per la bottega, con le seguenti sezioni/funzionalità:

- **Catalogo** prodotti (ceramiche in vendita, categorie, foto)
- **Storia** della bottega / artigiano
- **Info** pratiche (orari, contatti, come arrivare)
- **Google Maps** — mappa integrata con la posizione della bottega
- **Instagram** — link/embed alla pagina ufficiale

## Note di comunicazione
Il cliente/utente richiede risposte professionali e dirette al punto, senza fronzoli. Non usare tono "caveman" in questo progetto: qui prevale la richiesta esplicita di comunicazione professionale.

## Stack e decisioni tecniche
- Sito statico multi-pagina (HTML/CSS puro, no framework/build step): `index.html`, `catalogo.html`, `storia.html`, `contatti.html`, `grazie.html`, CSS condiviso in `css/style.css`
- Hosting: **Netlify**
- Form contatti: **Netlify Forms** (attributo `data-netlify="true"` sul form in `contatti.html`, redirect post-invio a `grazie.html`, honeypot anti-spam)
- Font: Fraunces (display) + Archivo (corpo), via Google Fonts
- Palette e loghi reali del brand (bordeaux `#8A3149`) — vedi `assets/img/`

## Stato progetto
Repo git locale (`carpediem/`, remote `github.com/ilBarlo/carpediem.git`), nessun commit ancora fatto. Struttura sito e design system definiti; in attesa di foto prodotto per il Catalogo.
