# programa-falla
Programa en Python de gestió de la Falla Sants Patrons

## 1. Introducció
La creació d'aquest programa per al control de l'oficina de la falla apareix, en un principi, per la falta d'opcions en el programa actual. El fet que les rifes, les domiciliacions, les loteries, les quotes o els descomptes familiars s'hagen de passar manualment comporta una pèrdua de temps molt important de cara a dur una correcta gestió de la falla. Si a això afegim el fet de que el programa (i el pc on s'executa) te molts anys i no hi ha copia de seguretat, es una raó molt important com per a ficar-se mans a l'obra per a construir un programa més estable, actual, portable i, sobretot, amb moltes més opcions i automatismes.

El programa s'ha d'encarregar de les següents tasques:
- Donar d'alta i baixa fallers.
- Agrupar els fallers per famílies.
- Crear un exercici nou en el que es calculen automàticament les quotes per edat, els descomptes familiars i el pendent o sobrant de l'any anterior de forma que mostre directament la quota final a pagar.
- Assignar automàticament les rifes a aquells fallers que els toque per edat quan ho requerisca l'administrador.
- Calcular automàticament els pagaments de loteria i els beneficis derivats de la venda a partir de les dades d'arreplega de loteria de cada faller ingressada al sistema per l'administrador.
- Controlar els pagaments de quota, loteria i rifa realitzats pels fallers tant en metàl·lic com per ingrés bancari o domiciliació.
- Crear i mantenir automàticament l'historial de cada faller i poder-lo modificar manualment en cas que siga necessari.

## 2. Descripció del problema
Hem de crear una aplicació d'escriptori amb la qual gestionar el dia a dia d'una associació amb un volum alt d'associats, de forma que pugam dispossar de la major quantitat possible d'automatismes que ens ajuden a realitzar les diferents gestions d'una forma fàcil, ràpida i segura.

## 3. Objectius
L'objectiu principal es dur la gestió automatitzada de la falla a la seua màxima expressió. Hem de reduir al mínim els processos manuals que comporten errors en gestió d'assignacions, pagaments, cens d'associats, etc.

A més, necessitem que totes aquestes accions queden emmagatzemades, de forma que es puga tindre accés a qualsevol moviment de diners, alta, baixa o qualsevol gestió que s'haja fet en la falla en qualsevol exercici anterior.

A part d'això, tenim l'objectiu de poder traure informes en pdf o qualsevol altre format per a proveïr a secretaría o altre departament de l'associació del que puguen necessitar d'una forma ràpida i fiable.

## Estructura del projecte
Arxius, carpetes, etc i com estan organitzats

## Diagrama UML
A implementar

## Descripció de les classes
A implementar

## Esquema de la base de dades
A implementar

## Descripció de les taules i relacions
### **Base de dades: “falla.db”**
### Taula “faller”
Registra les dades personals del faller i es relaciona amb les taules “familia” i “categoria” de forma que un faller només pot estar en una família i una categoria però una família i una categoria contenen un o més fallers.

**id: integer not null, PRIMARY KEY**  
Clau principal, identificació del faller.

**nom: text**  
Nom del faller.

**cognoms: text**  
Cognoms del faller.

**naixement: date**  
Data de naixement del faller en format “dd-mm-aaaa”

**sexe: integer**  
Sexe del faller. Integer en lloc de boolean per tindre en compte més opcions en el 	futur.

**dni: text**  
DNI del faller.

**adreça: text**  
Adreça del faller.

**telefon: text**  
Telèfon del faller.

**alta: boolean**  
El faller es alta si el seu valor es “1“ i baixa si es “0“.

**correu: text**  
Correu electrònic del faller.

**idfamilia: integer not null, FOREIGN KEY REFERENCES “familia” (“id”)**  
Identificador de la família del faller. Es relaciona amb l’identificador de la taula 	“familia” per a crear la relació entre les dues taules.

**idcategoria: integer not null, FOREIGN KEY REFERENCES “categoria” (“id”)**  
Identificador de la categoria del faller. Es relaciona amb l’identificador de la taula 	“categoria” per a crear la relació entre les dues taules.

### Taula: “categoria”
Registra les diferents categories de faller disponibles a la falla amb les seues condicions particulars.

**id: integer not null, PRIMARY KEY**  
Clau principal, identificació de la categoria.

**quota: integer**  
Quota que ha de pagar el faller segons la categoria a la que correspon.

**nom: text**  
Nom de la categoria

**descripcio: text**  
Breu descripció del rang d’edat al qual correspon la categoria.

### Taula: “familia”
Registra les famílies apuntades a la falla amb dades referents a la unitat familiar completa.

**id: integer not null, PRIMARY KEY**
Clau principal, identificació de la família.

**descompte: integer**
Descompte que s’efectua sobre la quota per quantitat de membres en la família.

**domiciliacio: boolean**
Informa si la quota familiar està o no domiciliada.

### Taula: “moviment”
Registra cada moviment que efectua un faller, d'assignació o pagament, siga de quota, rifa o loteria; i les dades necessàries per a la seua gestió.

**id: integer not null, PRIMARY KEY**  
Clau principal, identificació del moviment.

**data: text**  
Data en la quan es realitza el moviment. Es guarda en format “dd-mm-aaaa”.

**quantitat: real**  
Quantitat de diners en € corresponents al moviment.

**tipo: integer**  
Amb el valor “1“ correspon a una assignació i amb el valor “2“ serà un pagament.

**concepte: integer**  
El valor “1“ correspon a quota, el “2“ a loteria i el “3“ a rifa.

**exercici: integer**  
Mostra l’any en format “aaaa“ de l’exercici en que s’ha fet el moviment.

**descripcio: text**  
Breu descripció del moviment.

**rebut: integer**  
Número de rebut en cas de ser necessari (si es paga per caixa).

**idfaller: integer not null, FOREIGN KEY REFERENCES “faller” (“id”)**  
Identificador del faller que efectua el  moviment. Es relaciona amb l’identificador 	de la taula “faller” per a crear la relació entre les dues taules.

## Consultes a la base de dades
A implementar

## Arxius de text i les seues lectures/escriptures
A implementar

## 4. Instruccions d'instal·lació i requisits
Per a poder utilitzar el programa podeu descarregar el seu codi des del github del projecte [**programa-falla**](https://github.com/sethivan/programa-falla), on teniu el projecte complet per a poder-lo utilitzar lliurement al igual que podeu modificar dit codi per a adequar-lo a les vostres necessitats o per a afegir funcionalitats. En tal cas estaria molt agraït de que m'ensenyeu aquestes modificacions per si em son utils a mi tambè.

Una vegada descarregat el codi, necessiteu fer ús del llenguatje de programació amb el que l'he creat per a obrir el programa. Aquest llenguatje és Python i podeu descarregar_se'l des de la [**web oficial**](https://www.python.org/).

En aquest moment, i com podeu vore en les següents importacions, el programa utilitza dos llibreries externes que haurem d'instal·lar per al seu correcte funcionament: [**Pillow**](https://pypi.org/project/Pillow/) i [**reportlab**](https://pypi.org/project/reportlab/).

```python
from PIL import Image, ImageTk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
```

La llibreria Pillow és l'encarregada de gestionar les imatges en el sistema de finestres utilitzat (tkinter) i la llibreria reportlab és amb la qual creem els informes en .pdf.

Per a utilitzar-les només heu d'acudir a la terminal i instal·lar-les a través de pip.

Habitualment, amb la descàrrega de Python teniu el pip inclós però, en cas que no siga així, el podeu descarregar en el següent [enllaç](https://bootstrap.pypa.io/get-pip.py). Ara simplement acudiu en la terminal on heu descarregat l'arxiu i executeu:
>python get-pip.py

Una vegada teniu el pip instal·lat, només heu d'executar les següents instruccions des de la terminal per a descarregar les llibreries:
>pip install Pillow

>pip install reportlab

Ara únicament heu d'accedir a la terminal i, des d'allí, accedir a la carpeta on heu copiat el codi. Amb la següent instrucció fiqueu en marxa el programa:

>python programa_falla.pyw

Una altra opció més còmoda és utilitzar un programa de gestor de codi com poden ser [**Sublime text**](https://www.sublimetext.com/) o [**Visual Studio Code**](https://code.visualstudio.com/).

En un futur, quan ho crega convenient, crearé un .exe per a que siga més fàcil utilitzar el programa per a un usuari novell.

## Instruccions d'ús i exemples
A implementar

## Codi
A implementar

## Crèdits, llicència i contribucions
A implementar

## Estat del projecte
A implementar

## Contacte
A implementar