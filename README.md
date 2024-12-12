## README

This repo consists of the code and data used in my thesis project for the MSc in IT & Cognition at the University of Copenhagen. The project investigated the authorship of the Libro de los Epitomes. Specifically, NLP techniques and unsupervised machine learning algorithms were used to attempt to determine the number of distinct authors/writing styles present in the epitomes.

### Structure

The repo consists of a few different folders.

- Data folders:
  - epitomes
  - MedLatin
  - annotation

The epitomes-folder contains plain text transcriptions of the Libro de los Epitomes. The MedLatin-folder is more or less the same in that it contains the MedLatin dataset, which is a corpus of various Latin texts from medieval Italian writers. The annotation folder contains part-of-speech tag annotations made to measure the accuracy of CLTK's PoS-tagger.

- Script folders:
  - MedLatin-scripts
  - epitomes-scripts
 
These folders mainly contain Python notebooks which were used to run the experiments for the thesis. The scripts are named according to which experiment they pertain. I.e. those that have concordance in their name were used to run concordance experiments. Each folder also has a csvfiles subfolder where the style vector representations of the texts are saved.

- Figure folders:
  - plots
 
This folder contains png files with the saved figures used in the thesis.

### Running the notebooks

To run the notebooks, create a venv and install the packages in the requirements file. (It may be necessary to downgrade pip to 21.3.1, since there were some issues getting CLTK to work otherwise. On the other hand, that issue might now be fixed.)
