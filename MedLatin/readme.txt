==========================================
README
==========================================

This file contains MedLatin1 and MedLatin2 corpora.
The structure is as follows:

\-- ./Corpora/
    \-- MedLatinEpi : 294 epistolary texts from different Latin authors
    \-- MedLatinLit : 30 non-epistolary texts from different Latin authors
\-- ./Epistle/ : 
	the first part of epistle XIII (EpistolaXIII_1.txt) and
	the second part (EpistolaXIII_2.txt). The epistles are 
	also split in paragraphs (e.g., EpistolaXIII_1_10.txt is
	the 10th paragraph of the first part of the epistle). 
	There are 13 paragraphs for the first part and 90 paragraphs 
	for the second part. We also include Epistola_ArigoVII.txt, 
	as an additional example for testing the verifier.
\-- ./Results/ : 
    all the results of the experiments we conducted. There are 3 types of file:
    - resultsLOO_{corpus}_{method}.txt : the file contains the results of the 
        LOO experiment with the specified {method} on the specified {corpus}. 
        There are the results for the single verifier by author (F1, accuracy, 
        confusion matrix, texts misclassified) and the final aggregated 
        results (Macro-F1, Micro-F1, accuracy).
    - resultsUNK_{epistle}_{part}_{method}.txt : the file contains the result of
        the classification experiment with the specified {method} on the {epistle}
        (only on the single {part}, when specified), only for the author Dante.
    - results_doc_by_author.ods : contingency table by author, diplaying the 
        results of the LOO experiments with Logistic Regressor.
