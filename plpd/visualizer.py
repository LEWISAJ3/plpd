import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
class Visualizer():
    def __init__(self,data=None):
        self.data=data
    def PCA(self,data=None,encode=True,color=None,size=None,omit=None):
        if data is None:
            data=self.data
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler
        omitdata=data
        if omit:
            omitdata=data.drop(columns=omit)
        data_dummy=omitdata
        
        if encode:
            data_dummy=pd.get_dummies(omitdata,drop_first=True)
        SS=StandardScaler()
        fit_data=SS.fit_transform(data_dummy)
        pca=PCA(n_components=2)
        data_pc=pca.fit_transform(fit_data)
        data_df=pd.DataFrame(data_pc,columns=["pc1","pc2"])
        
        import seaborn as sns
        import matplotlib.pyplot as plt
        if not color is None:
            data_df[color]=data[color]
        if not size is None:
            data_df[size]=data[size]
        sns.scatterplot(
            data=data_df,
            x="pc1",
            y="pc2",
            hue=color,
            size=size,          # continuous variable
            palette="viridis",
              sizes=(2,20)  # any matplotlib colormap
        )

        plt.show()
        return data_pc
    def scatterplot(self,data=None,x=None,y=None,color=None,size=None):
        if data is None:
            data=self.data
        
        
        sns.scatterplot(
            data=data,
            x=x,
            y=y,
            hue=color,
            size=size,          # continuous variable
            palette="viridis",
              sizes=(2,20)  # any matplotlib colormap
        )
        plt.show()
    def aggplot(self,data=None,value=None,groups=None):
        if data is None:
            data = self.data
        # Step 1: aggregate the values (mean per group)
        agg = data.groupby(groups)[value].mean().reset_index()

        # Step 2: plot
        plt.figure(figsize=(6,5))
        sns.scatterplot(
            data=agg,
            x=groups[0],
            y=groups[1],
            size=value,        # size of dot proportional to mean
            sizes=(50, 500),     # min and max point size
            legend='brief',
            alpha=0.7
        )

        plt.title('Bubble Plot by Category')
        plt.show()
        
    
        

