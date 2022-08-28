# Structure-Prediction-
##Notebooks and data used for crystal structure prediction of inorganic compounds using composition based feature vectors

An ionic substitution model inspired by the work of Hautier et al. was used for the structure prediction. This model has been implemented within the open source python package SMACT, developed by Walsh Materials Design (WMD) group [https://github.com/WMD-group/SMACT](https://github.com/WMD-group/SMACT). 

The paper from Hautier et al. proposing the original ionic substitution model can be found [here](https://doi.org/10.1021/ic102031h)

The three composition based feature vectors used for structure prediction in this project are:
1. SkipAtom - [Distributed representations of atoms and materials for machine learning ](https://doi.org/10.1038/s41524-022-00729-3)
            - [github](https://github.com/lantunes/skipatom)
2. MatScholar - [Named Entity Recognition and Normalization Applied to Large-Scale Information Extraction from the Materials Science Literature](https://doi.org/10.1021/acs.jcim.9b00470)
3. Magpie - [A general-purpose machine learning framework for predicting properties of inorganic materials ](https://doi.org/10.1038/npjcompumats.2016.28)

The results from this project were used to write my MSc thesis at Imperial College London. Thanks to Prof. Aron Walsh for introducing me to this field, and thanks to Anthony Onwuli for his support with code and analysis. 
