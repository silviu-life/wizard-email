---
name: mail-sync
description: Citește Gmail și creează sau actualizează fișele din `contacte/<email>/` (profile.md + istoric.md). Folosește la `/mail sync [--zile N] [query]`, „citește inbox-ul", „cine mi-a scris", „adu emailurile", „sincronizează contactele", „importă tot istoricul de emailuri", sync inbox, pull emails, who emailed me. Ia doar corespondență reală, om-cu-om; sare peste advertising, marketing, newslettere, notificări. Nu clasifică (`mail-classify`), nu scrie drafturi (`mail-draft`), nu procesează (`mail-process`).
---

# /mail sync — inbox → contacte/

Citește `reguli/schema.md` (secțiunile `profile.md` și `istoric.md`) înainte să scrii orice.
Adresa proprie: din `firma/profil.md` („Email propriu"). Fără ea, oprește-te și cere-o.

## Pas 1 — intervalul și query-ul

- `--zile N`: default **360**. „ultimele 3 zile" → `--zile 3`.
- Query implicit (Gmail îl filtrează el, ieftin):
  ```
  newer_than:<N>d -category:promotions -category:social -category:updates -category:forums -in:spam -in:trash
  ```
  Dacă utilizatorul dă un query Gmail, îl **adaugi** la cel implicit, nu îl înlocuiești (filtrele
  anti-marketing rămân). Include `in:sent`? Nu: istoricul e despre ce primești. Mesajele tale din
  thread-uri primite se văd oricum prin `get_thread`.

## Pas 2 — listează thread-urile, în loturi

Unealta Gmail `search_threads` cu `query`, `view: THREAD_VIEW_MINIMAL`, `pageSize: 50`. Paginează cu
`pageToken`. La 360 de zile pot fi sute de pagini: **procesezi complet fiecare pagină (pașii 3-4) înainte
să ceri următoarea**, ca o întrerupere să lase fișele consistente. Dedupe-ul după `msg:<id>` face
rularea reluabilă: a doua rulare sare peste ce există deja.

## Pas 3 — filtrul anti-marketing, per thread (obligatoriu, înainte de get_thread)

Un thread e **sărit** dacă oricare e adevărat, verificat pe câmpurile din listă (sender, subject, snippet):
1. Expeditorul se potrivește pe: `noreply`, `no-reply`, `donotreply`, `notification`, `notifications`,
   `mailer-daemon`, `newsletter`, `news@`, `info@`, `hello@`, `marketing@`, `promo`, `offers@`, `team@`,
   `support@`, `billing@`, `invoice@`, `@calendar-`, `@docs.google.com`, `@accounts.`, `@mail.`, `@em.`,
   `@e.`, `@bounce`, `@sendgrid`, `@mailchimp`, `@hubspot`, `@klaviyo`, `@substack`, `@medium.com`,
   `@linkedin.com`, `@facebookmail.com`, `@notion.so`, `@slack.com`, `@github.com`, `@stripe.com`,
   `@paypal.com`, plus orice adresă/domeniu din lista „Ignoră" din `firma/profil.md`.
2. Subiectul sau snippet-ul conține: „dezabonare", „unsubscribe", „newsletter", „webinar gratuit",
   „ofertă specială", „reducere", „% off", „black friday", „ultimele ore", „nu rata", „confirmă adresa",
   „verify your email", „your order", „comanda ta", „factura ta", „receipt", „invoice #", „password",
   „parola", „cod de verificare", „security alert", „digest", „weekly", „săptămânal", „roundup".
3. Thread-ul are un singur mesaj, iar `to_recipients` nu conține adresa ta direct (ești în bcc / listă).
4. Singurul expeditor din thread ești tu.

Un thread trece dacă scapă de toate patru. Dacă nu ești sigur (ex. `contact@firma.ro` care scrie
personal), **trece**: e mai ieftin un contact în plus decât un client pierdut. Numără cât ai sărit, pe
motiv, pentru raport.

## Pas 4 — per thread relevant

`get_thread` cu `messageFormat: PLAIN_TEXT`. Pentru fiecare adresă expeditoare ≠ a ta (lowercase):

- `contacte/<email>/` **nu există** → creează `profile.md` după schemă: `email`, `nume` (din display name
  al header-ului From; gol dacă lipsește), `sursa: gmail`, `creat` = data primului mesaj de la el,
  `stadiu: nou`, restul gol. Secțiunile din corp goale. Creează `istoric.md` gol.
- **există** → schimbi doar `actualizat` (= azi) și `ultima_interactiune` (= data celui mai nou mesaj primit).

Verificare a doua, pe corp: dacă textul conține link de dezabonare sau e evident un template de masă
(fără nicio referire la tine, la firma ta, la o discuție), **nu** creezi contactul; îl numeri la „sărite
după corp".

Apoi `istoric.md`: pentru fiecare mesaj al contactului al cărui `msg:<id>` NU apare deja în fișier:
```
## <data mesajului> · primit · "<subiect>" · thread:<threadId> · msg:<messageId>
<2-3 linii: ce cere, ce semnale (buget, urgență, obiecție, întrebare de preț)>
```
Mesajele tale din același thread se adaugă ca `## <data> · trimis · "<subiect>" · thread:<id> · msg:<id>`
cu o linie de rezumat, ca istoricul să reflecte conversația reală (importate, nu prin `mail-send`).
Intrările se pun în ordine cronologică.

## Pas 5 — index și raport

`python3 scripts/index.py`. Raport:
- contacte noi / actualizate / mesaje adăugate;
- thread-uri sărite, pe motiv (expeditor / subiect / bcc / doar eu / corp);
- „N contacte au `tip` gol → `/mail classify --toate`"; „M emailuri neprocesate → `/mail process`".
STOP.

## Ce NU faci
- Nu completezi `tip`, `segment`, personalitate. Nu ghicești nimic.
- Nu scrii drafturi, nu trimiți, nu pui etichete în Gmail, nu ștergi nimic.
