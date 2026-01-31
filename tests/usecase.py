from plpd import DataEditor,RegressionPipeline 
import pandas as pd
import numpy as np
data=pd.read_csv("C:/Users/Allen/OneDrive/Documents/kaggle1/train.csv")
print(data.head(5))
x=data.iloc[0:2000,:]
x.iloc[0:15,[1,3,4]]=np.nan
x.iloc[10:20,[1,5,7]]=np.nan
de=DataEditor(x)
de.handle_missing()
rp=RegressionPipeline()
rp.lazy_regression(de.data,"exam_score")
de.detect_nominal()
rp.lazy_regression(de.data,"exam_score")



