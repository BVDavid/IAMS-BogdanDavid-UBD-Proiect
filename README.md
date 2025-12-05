# 📦 IAMS - Inventory & Asset Management System

Proiect realizat pentru disciplina **Utilizarea Bazelor de Date (UBD)**.

**IAMS** este o aplicație web completă pentru gestionarea inventarului IT (calculatoare, laptopuri, servere) și a componentelor hardware asociate. Aplicația demonstrează utilizarea unei baze de date relaționale complexe (PostgreSQL), containerizare (Docker) și o interfață web intuitivă (Flask + Bootstrap).

---

## 🚀 Funcționalități Principale

1.  **Gestiunea Echipamentelor (CRUD):** Adăugare, vizualizare, filtrare și ștergere echipamente.
2.  **Componente Hardware (Relație Many-to-Many):** Asocierea și dezasocierea componentelor (CPU, RAM, HDD) de pe un echipament specific.
3.  **Autentificare și Roluri:**
    * **Admin:** Are drepturi depline (poate șterge orice, poate adăuga echipamente pentru alți utilizatori).
    * **User:** Poate vedea tot inventarul, dar poate modifica/șterge *doar* echipamentele proprii.
4.  **Validarea Datelor:** Protecție împotriva datelor invalide (format IP, Hostname, Serial Number unic).
5.  **Filtrare Avansată:** Filtrarea echipamentelor în funcție de locația fizică (Room, Server Room, etc.).

---

## 🛠️ Cerințe Preliminare (Prerequisites)

Pentru a rula acest proiect, ai nevoie doar de **Docker** instalat.

* **Docker Desktop** (Windows/Mac) sau **Docker Engine** (Linux).
* **Git** (pentru a descărca proiectul).

Verifică dacă ai Docker instalat rulând în terminal:
```bash
docker --version
docker compose version
⚙️ Instalare și RulareUrmează acești pași simpli pentru a porni aplicația în câteva minute:1. Clonează RepozitoriulDeschide un terminal și descarcă proiectul:Bashgit clone [https://github.com/BVDavid/IAMS-BogdanDavid-UBD-Proiect.git](https://github.com/BVDavid/IAMS-BogdanDavid-UBD-Proiect.git)
cd IAMS-BogdanDavid-UBD-Proiect
2. Pornește Aplicația (Build & Run)Rulează comanda de mai jos pentru a construi imaginile și a porni containerele:Bashdocker compose up -d --build
Notă: Prima rulare poate dura 1-2 minute pentru a descărca imaginile de Python și PostgreSQL.3. Accesează AplicațiaDeschide browserul și navighează la:👉 http://localhost:5000🔐 Credențiale de Acces (Login)Baza de date este populată automat cu doi utilizatori pentru testare:RolEmailParolaDrepturiADMIN 👑bogdandavid.work@gmail.comadmin123Acces Total (Adăugare/Ștergere orice).USER 👤user@test.comuser123Read-Only pe alții, Full Access pe propriile asset-uri.🧪 Ghid de Testare (Scenarii)Pentru a evalua funcționalitățile proiectului, parcurgeți următoarele scenarii:Scenariul 1: Administrare Completă (Login ca Admin)Loghează-te cu contul de Admin.Apasă "Adaugă Echipament". Completează datele (alege un User diferit din listă).Observă validările: Încearcă să pui un IP greșit (ex: 999.999.999) -> Vei primi eroare.După salvare, intră la Detalii pe echipamentul creat.Folosește formularul din stânga pentru a asocia o componentă (ex: un CPU).Componenta apare în tabelul din dreapta. Apasă pe X roșu pentru a o șterge.Mergi în Dashboard și șterge echipamentul folosind butonul Gunoi.Scenariul 2: Restricții User (Login ca User)Dă Logout și loghează-te cu contul de User.În Dashboard, vei observa că NU poți șterge echipamentele care aparțin lui "David Bogdan" (nu apare butonul de ștergere).Adaugă un echipament nou. Vei observa că nu poți alege proprietarul (ești asignat automat).Intră la Detalii pe un echipament al Adminului -> Vei primi mesajul "Acces Interzis".Scenariul 3: FiltrareÎn Dashboard, selectează din dropdown "Server Room" și apasă Aplică.Lista se va actualiza afișând doar serverele din acea cameră.📂 Structura Proiectuluidocker-compose.yml: Fișierul principal de orchestrare. Definește serviciile db (PostgreSQL) și backend (Flask).Dockerfile: Instrucțiunile pentru construirea imaginii aplicației Python.init-scripts/:01_create_tables.sql: Crearea structurii bazei de date (DDL).02_insert_data.sql: Popularea inițială cu date de test (DML).app/:app.py: Logica backend (rute, conexiune DB, validări).templates/: Fișierele HTML (Frontend cu Bootstrap).❓ Troubleshooting (Probleme Comune)Q: Primesc eroare la pornire sau baza de date pare goală.R: Dacă ai rulat proiectul anterior cu o schemă veche, Docker poate păstra volumul vechi. Resetează totul cu comanda:Bashdocker compose down -v
docker compose up -d --build
(Atenție: Aceasta șterge toate datele adăugate manual și re-inițializează baza de date cu datele din scripturi).
