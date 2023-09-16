
<h1>Diplomski rad</h1>

<h2>Sustav za preporučivanje smještaja u sklopu sjedišta turističke agencije</h2>

Autor: Domagoj Muža

Mentor: doc. dr. sc. Nikola Tanković

Sveučilište Jurja Dobrile u Puli, Fakultet informatike


<h3>Sažetak</h3>

Razlog za implementaciju sustava je došao iz potrebe za poboljšanjem korisničkog iskustva i boljeg plasmana smještaja kupcima, bili oni novi ili već postojeći.
Sustav je implementiran koristeći KNN model i model matrične faktorizacije. Razlog za korištenje dva modela dolazi iz činjenice da velik broj korisnika prvi put posjećuje stranicu [www.istriasun.com](https://www.istriasun.com/istra) te nemamo zapise o njemu, odnosno ne možemo personalizirati preporuku.




<h3>Modeli</h3>
  
<h4>KNN</h4>

- KNN koristimo kada nemamo dovoljno podataka o korisniku. Služi za preporuku baziranoj na artiklu (u našem slučaju je to smještajna jedinica), a radi na način da kada korisnik otvori stranicu o pojedinoj smještajnoj jedinici sustav daje preporuku baziranu na prijašnjim interakcijama korisnika s drugim smještajnim jedinicama. 


<h4>Matrična faktorizacija</h4>

- Matričnu faktorizaciju koristimo za personaliziranu preporuku postojećim korisnicima. U slučaju web stranice to su korisnici koji su povezani sa jednom ili više rezervacija. Da bi došli do preporuke model će izračunati latentne faktore te na osnovu njih predviđamo koje smještajne jedinice bi korisnik mogao rezervirati, a koje pregledati (otvoriti stranicu o smještajnoj jedinici).


<br/>

Cijeli rad se može pročitati [OVDJE](https://github.com/DomagojMuza/Diplomski/blob/main/Diplomski.pdf)