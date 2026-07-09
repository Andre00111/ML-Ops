# PDF Export Anleitung für PIPELINE_GUIDE

Du hast zwei Versionen:
- `PIPELINE_GUIDE.md` (Markdown - Text)
- `PIPELINE_GUIDE.html` (HTML - Formatiert & schön)

## Option 1: HTML → PDF (Empfohlen - sieht am besten aus)

### Via Browser (easiest)

1. **Öffne die Datei:**
   ```bash
   open PIPELINE_GUIDE.html
   # oder im Browser: File → Open → PIPELINE_GUIDE.html
   ```

2. **Export als PDF:**
   - **macOS/Chrome:** Cmd + P → "Save as PDF" → "Save"
   - **macOS/Safari:** Cmd + P → PDF (unten links) → "Save as PDF"
   - **Windows/Chrome:** Ctrl + P → "Save as PDF" → "Save"
   - **Firefox:** Ctrl + P → "Print to File" → Format: PDF

3. **Fertig!** PDF wird zu `~/Downloads/PIPELINE_GUIDE.pdf` gespeichert

---

### Via Command Line (optional)

Falls du auf macOS wkhtmltopdf installiert hast:

```bash
# Install (falls nicht vorhanden)
brew install wkhtmltopdf

# Convert
wkhtmltopdf PIPELINE_GUIDE.html PIPELINE_GUIDE.pdf

# Verify
ls -lh PIPELINE_GUIDE.pdf
```

---

## Option 2: Markdown → PDF

Falls du die Markdown-Version bevorzugst:

```bash
# Install pandoc
brew install pandoc

# Convert
pandoc PIPELINE_GUIDE.md -o PIPELINE_GUIDE.pdf

# Mit besserer Formatierung
pandoc PIPELINE_GUIDE.md \
  -V geometry:margin=1in \
  -V fontsize=10pt \
  --toc \
  -o PIPELINE_GUIDE.pdf
```

---

## Qualität vergleichen

| Format | Qualität | Formatierung | Tabellen | Farben |
|--------|----------|---|---|---|
| **HTML** | ⭐⭐⭐⭐⭐ Beste | ✓ Perfekt | ✓ Gut | ✓ Ja |
| **Markdown** | ⭐⭐⭐ Gut | ⚠️ Basic | ⚠️ Plain | ✗ Nein |

**Empfehlung:** HTML → Browser → Print to PDF

---

## Troubleshooting

### "wkhtmltopdf not found"
```bash
brew install wkhtmltopdf
# Dann nochmal versuchen
```

### "Chrome not found"
```bash
# Installiere Chrome von https://google.com/chrome
# oder nutze die Browser-Methode oben
```

### PDF sieht komisch aus
→ Nutze die Browser "Print to PDF" Methode statt Command Line

---

## Fertig!

Deine PDF ist jetzt bereit zum:
- 📧 Verschicken an Kolleg:innen
- 🖨️ Ausdrucken
- 📚 Archivieren
- 📖 Offline Lesen

