# Projektni Zadatak 1 – Load Balancer
## res-tim-1-ftn

Potrebno je napraviti dizajn sistema, arhitekturu sistema, implementira i istestirati rešenje koji simulira rad i komunikaciju Load Balancer modula.
Sistem sadrži 4 komponente:
1. **Writer**
2. **Load Balancer**
3. **Worker**
4. **Database CRUD**

# Writer

Writer je komponenta koja služi za upisivanje novih podataka u Load Balancer komponentu.
Writer komponenta šalje nove podatke Load Balancer komponenti. Writer takođe ima opciju paljenja i gašenja Workera sa kojima Load Balancer radi, kao i manuelnog slanja podataka.
Writer komponenta šalje podatke o očitanim vrednostima sa kućnih brojila.
Podatak koji se šalje sadrži informaciju o ID-ju komponente i vrednosti koja je ocitana (trenutna potrošnja brojila) Neophodno je obezbediti pokretanje N instanci writer-a.

# Load Balancer

Load Balancer je komponenta koja služi za ravnomerno raspoređivanje posla.
Posao raspoređuje Workerima.
Load Balancer prima podatke od Writer komponente i prosleđuje ih nekom od slobodnih Workera na obradu.
Load Balancer privremeno smešta podatke kod sebe (u buffer) i nakon prikupljnih 10 vrednosti te podatke prosledjuje prvom slobodnom workeru.

# Worker

Worker je komponenta koja služi za obradu podataka dobijenih od Load Balancer komponente.
Worker komponenta podatke dobijene od Load Balancer komponente snima u bazu posredstvom Database CRUD komponente.
Neophodno je voditi racuna o tome ako worker pokuša da upiše vrednost u isti red u bazi.

# Database CRUD

DatabaseCRUD komponenta služi za svu komunikaciju koja se obavlja sa bazom podataka i ova komponenta je zadužena za izvršavanje CRUD operacija.
Baza podataka treba da sadrzi jednu tabelu u kojoj će se nalaziti informacije o odredjenom brojilu.
(ID brojila, ime i prezime korisnika, ulica, broj, postanski broj, grad) i jednu tabelu u kojoj se belezi potrošnja brojila(ID brojila, potrosnja, mesec)

# Database Analitics

Database Analitics komponenta komunicira sa DatabaseCRUD kompoentom i služi za izvlacenje statistika iz baze podataka u vidu dva tipa izvestaja, jedan je potrosnja po mesecima za odredjeni grad, a drugi je potrosnja po mesecima za konkretno brojilo.