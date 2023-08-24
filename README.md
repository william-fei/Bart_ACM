# ac-monitor
Public facing git repo; all proprietary source files, data, and sensitive info removed
 

The commit "Final changes" ede9ab0 on the main branch contains the latest presentable for UCB Data Discovery showcase. The meaningful artifacts are:
- src/notebooks/aclabeler.py :: defines class ACLabeler
- src/notebooks/AC_labeler.ipynb :: the notebook to perform labelling sample data using ACLabeler call defined in src/notebooks/aclabeler.py
- notebooks/BART-ecg-anomaly-detection.ipynb :: anomaly detection with
  autoencoder and LSTM. It is renamed to ac_anomaly_detection.{py, ipynb}
  respectively in notebooks and scripts sub-folders in the annotation process
- data/tempseries_labeled.zip :: first 3 rows (out of 129760) of the actual labeled time series data used in BART-ecg-anomaly-detection.ipynb
- data/labeledtimewindows/labeledtimewindows_ab_yuan.zip :: first five rows of the labels done by Steven Yuan
- data/labeledtimewindows/labeledtimewindows_william.zip :: first five rows of the labels done by William Fei
- data/labeledtimewindows/labeled_timewindows_conflict_yuanwilliam :: first five rows of the labels done by Floyd
- data/abeledtimewindows_all.zip :: the combination of labels from Steven,
  William and Floyd