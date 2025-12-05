# 📦 IAMS - Inventory & Asset Management System

Proiect realizat pentru disciplina **Utilizarea Bazelor de Date (UBD)**.

**IAMS** este o aplicație web completă pentru gestionarea inventarului IT (calculatoare, laptopuri, servere) și a componentelor hardware asociate. Aplicația demonstrează utilizarea unei baze de date relaționale complexe (PostgreSQL), containerizare (Docker) și o interfață web intuitivă (Flask + Bootstrap).

---

## 🚀 Funcționalități Principale

### 1. Gestiunea Echipamentelor (CRUD Complet)
* **Adăugare:** Formular complex cu validări pentru IP și Serial Number unic.
* **Vizualizare:** Dashboard cu listare tabelară și statusuri colorate.
* **Ștergere:** Posibilitatea de a șterge echipamente (cu protecție `ON DELETE CASCADE` în baza de date).

### 2. Componente Hardware (Relație Many-to-Many)
* **Asociere:** Posibilitatea de a adăuga componente (CPU, RAM, HDD) pe un echipament specific din pagina de detalii.
* **Dezasociere:** Ștergerea componentelor de pe un echipament.

### 3. Securitate și Roluri
* **Admin:** Are drepturi depline (poate șterge orice, poate adăuga echipamente pentru alți utilizatori).
* **User:** Poate vedea tot inventarul, dar poate modifica/șterge *doar* echipamentele proprii.

### 4. Funcții Avansate
* **Filtrare:** Filtrarea echipamentelor în funcție de locația fizică (Room, Server Room, etc.).
* **Paginare:** Componentele din dropdown sunt paginate pentru performanță.
* **Validare:** Protecție backend și frontend împotriva datelor invalide.

---

## 🛠️ Tehnologii Utilizate

* **Docker & Docker Compose:** Pentru containerizare și orchestrarea serviciilor.
* **PostgreSQL 15:** Baza de date relațională.
* **Python 3.11 + Flask:** Framework pentru Backend.
* **Bootstrap 5:** Framework CSS pentru interfață.
* **Psycopg2:** Driver pentru conectarea Python la PostgreSQL.

---

## ⚙️ Instalare și Rulare

Ai nevoie doar de **Docker** instalat.

### 1. Clonează Repozitoriul
Deschide un terminal și rulează:
```bash
git clone https://github.com/BVDavid/IAMS-BogdanDavid-UBD-Proiect.git
cd IAMS-BogdanDavid-UBD-Proiect
```

### 2. Pornește Aplicația
Rulează comanda de mai jos în terminal, în folderul proiectului:

```bash
docker compose up -d --build
```
Notă: Prima rulare poate dura 1-2 minute pentru descărcarea imaginilor.

### 3. Accesează Aplicația
Deschide browserul și intră pe: 👉
```bash
http://localhost:5000
```

### 🔐 Conturi pentru Testare
Baza de date este populată automat cu acești utilizatori:

| Rol | Email | Parola | Drepturi |
| :--- | :--- | :--- | :--- |
| **ADMIN** 👑 | `bogdandavid.work@gmail.com` | `admin123` | Acces Total. |
| **USER** 👤 | `user@test.com` | `user123` | Doar pe asset-urile proprii. |
### 📂 Structura Proiectului

```bash
iams-project/
├── docker-compose.yml       # Configurare Servicii (DB + App)
├── Dockerfile               # Configurare Imagine Python
├── requirements.txt         # Dependențe (Flask, psycopg2)
├── init-scripts/            # Scripturi SQL rulare automată
│   ├── 01_create_tables.sql # Schema Bazei de Date (DDL)
│   └── 02_insert_data.sql   # Date Inițiale (DML)
└── app/
    ├── app.py               # Codul sursă Backend
    └── templates/           # Interfața Grafică (HTML)
        ├── login.html
        ├── assets.html
        ├── add_asset.html
        └── asset_detail.html
```
### ❓ Troubleshooting
### Question:
   Primesc eroare "Internal Server Error" sau baza de date e goală. 
### Answer:
   Uneori Docker păstrează volumele vechi. Resetează totul cu comanda:

```bash
docker compose down -v
docker compose up -d --build
```

### Question:
   Nu mă pot conecta la localhost:5000. 
### Answer:
   Verifică dacă containerul rulează folosind docker compose ps. Dacă nu, verifică erorile cu docker compose logs backend.
