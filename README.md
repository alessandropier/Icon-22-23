# Progetto-ICon

Esame di Ingegneria della Conoscenza A.A. 2022/23 - Università degli Studi di Bari "Aldo Moro"

Membri:
- Alessandro Piergiovanni (MAT: 738044)
- Saverio de Candia (MAT: 736578)
- Nicolò Sciancalepore (MAT: 735589)

---

# Funzionalità del Sistema

Il progetto implementa un sistema completo per la predizione del PEGI di un videogioco attraverso l'apprendimento supervisionato utilizzando l'algoritmo Random Forest. Offre un sistema di raccomandazione di 10 giochi basato sull'input di un gioco dall'utente, utilizzando l'algoritmo K-Means per l'apprendimento non supervisionato. Inoltre, viene realizzata una base di cononscenza in Prolog e mediante 10 regole che operano sinergicamente sono state realizzate 7 query in grado di fornire ulteriori informazioni utili.

## Componenti Principali:
- **Predizione del PEGI:** Utilizza l'algoritmo Random Forest per prevedere il PEGI di un videogioco inserito in input.
- **Sistema di Raccomandazione:** Basato su K-Means, suggerisce 10 giochi correlati a quello inserito dall'utente.
- **Base di Conoscenza Prolog:** Composta da 10 regole specifiche, supporta 7 query per fornire ulteriori informazioni o analisi.

Il sistema offre una completa soluzione per la predizione del pegi dei giochi e per fornire raccomandazioni personalizzate agli utenti, sfruttando sia l'apprendimento supervisionato che non supervisionato, oltre a una vasta base di conoscenza Prolog per ulteriori analisi.

---

# Descrizione Repository

Dataset Utilizzati: 
- https://www.kaggle.com/datasets/gregorut/videogamesales
- https://www.kaggle.com/datasets/floval/jvc-game-reviews

<br>

La repository è composta dalle seguenti directory:
- Code: contiene tutti i codici utilizzati per la realizzazione del progetto, comprese le funzioni di preprocessing del dataset, funzioni per l'apprendimento supervisionato e non supervisionato e il prolog
- Dataset: contiene i due dataset originali e i dataset preprocessati utilizzati dalle funzioni di raccomandazione e predizione
- Documentazione: contiene la documentazione del progetto in formato Word (.docx) e PDF
- Images: contiene le immagini utilizzate per realizzare la documentazione di progetto
---
