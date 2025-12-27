# GitHub'a Workflow Değişikliklerini Yükleme Rehberi

## Seçenek 1: GitHub Web Arayüzünden (ÖNERİLEN) ✅

### .github/workflows/ci.yml için:

1. https://github.com/recepztrk/ymh429-sqa-api-test-framework/blob/main/.github/workflows/ci.yml adresine git
2. Sağ üstteki **✏️ Edit** butonuna tıkla
3. Dosyanın en sonuna (70. satırdan sonra) şu satırları ekle:

```yaml
      - name: Run smoke tests
        run: |
          pytest -m smoke -v --junitxml=junit-report.xml

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: pytest-results
          path: junit-report.xml
```

4. **Commit changes** butonuna tıkla
5. Commit message: "Add pytest execution and JUnit report upload"
6. **Commit changes** ile onayla

### api/main.py için:

1. https://github.com/recepztrk/ymh429-sqa-api-test-framework/blob/main/api/main.py adresine git
2. Sağ üstteki **✏️ Edit** butonuna tıkla
3. 119-141. satırlar arasındaki PATCH endpoint'i sil (@app.patch("/products/{id}") kısmını tamamen kaldır)
4. **Commit changes** butonuna tıkla
5. Commit message: "Remove unused PATCH /products/{id} endpoint"
6. **Commit changes** ile onayla

---

## Seçenek 2: SSH ile Push (Gelişmiş)

Eğer SSH key'in varsa:

```bash
# Git remote'u SSH'ye değiştir
git remote set-url origin git@github.com:recepztrk/ymh429-sqa-api-test-framework.git

# Push et
git add .github/workflows/ci.yml api/main.py
git commit -m "Complete CI workflow and remove unused endpoint"
git push origin main

# Sonra tekrar HTTPS'e dön
git remote set-url origin https://github.com/recepztrk/ymh429-sqa-api-test-framework.git
```

---

## Seçenek 3: Yeni Personal Access Token (PAT) Oluştur

1. GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. **Generate new token (classic)**
3. Adı: "Workflow Management"
4. ✅ **workflow** scope'unu seç (önemli!)
5. ✅ **repo** scope'unu seç
6. Generate token
7. Token'ı kopyala
8. Terminal'de:

```bash
# Token'ı kullanarak push et
git push https://YOUR_TOKEN@github.com/recepztrk/ymh429-sqa-api-test-framework.git main
```

---

## Hangi Seçeneği Öneriyorum?

**Seçenek 1 (Web Arayüzü)** - En hızlı ve kolay, 2 dakika sürer.

Bu değişiklikler kritik değil (CI zaten çalışıyor), ama eklenirse daha profesyonel olur.
