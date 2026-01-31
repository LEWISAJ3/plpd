from plpd import DataEditor
from plpd import RegressionPipeline
from plpd.visualizer import visualizer
import pandas as pd
import numpy as np
data=pd.read_csv("C:/Users/Allen/OneDrive/Documents/kaggle1/train.csv")
print(data.head(5))
x=data.iloc[0:2000,:].drop(columns=["id"])
#x.iloc[0:15,[1,3,4]]=np.nan
#x.iloc[10:20,[1,5,7]]=np.nan


de=DataEditor(x)
#de.convert_to_cat(col="exam_score",labels=["f","c","a"])
vs=visualizer(de.data)
vs.PCA(color="exam_score",omit="exam_score")
#vs.scatterplot(y="exam_score",x="study_hours",color="gender")
#vs.aggplot(value="exam_score",groups=["study_method","sleep_quality"])
#de.handle_missing()
#print(de.data)
#rp=RegressionPipeline()
#rp.lazy_regression(de.data,"exam_score")
#de.detect_nominal()
#rp.lazy_regression(de.data,"exam_score")



