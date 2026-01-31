import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np

class data_editor():
    
    def __init__(self,data):
        self.data=data
    def column_preview(self, col, n=3):
        df = self.data
        uniques = df[col].dropna().unique()[:n]
        values = ", ".join(map(str, uniques))
        return f"{col}: {values}"
    def detect_nominal(self,num=10):
        items=[]
        itemnames=[]
        for col in self.data.columns:
            if self.is_low_cardinality(self.data[col],num):
                items.append(col)
                itemnames.append(self.column_preview(col))
        selected=self.select_items_gui(items,itemnames)
        for selection in selected:
            unique_vals=set(self.data[selection])
            mapping,poly = self.assign_category_levels(selection,unique_vals)
            if mapping:
                self.data=self.encode_categorical(selection,mapping,poly).drop(columns=selection)
    def handle_missing(self):
        import missingno as msno
        import matplotlib.pyplot as plt
        from PIL import Image, ImageTk
        if self.data.isna().sum().sum()==0:
            print("No Missing Values!")
            return
        print(self.data.isna().sum())
        fig, axs = plt.subplots(2, 1, figsize=(5, 10))
        msngdata = self.data[self.data.columns[self.data.isna().any()]]
        msno.matrix(msngdata, ax=axs[0])
        msno.heatmap(msngdata, ax=axs[1])

        plt.tight_layout()
        plt.savefig("example.png")
        
        def mean_impute():
            num_cols = self.data.select_dtypes(include='number').columns
            cat_cols = self.data.select_dtypes(exclude='number').columns

            # numeric → mean
            self.data[num_cols] = self.data[num_cols].fillna(
                self.data[num_cols].mean()
            )

            # categorical → mode
            self.data[cat_cols] = self.data[cat_cols].fillna(
                self.data[cat_cols].mode().iloc[0]
            ) 
            
            root.destroy()
        def dropna():
            self.data=self.data.dropna()
            root.destroy()
        def dropnacolumns():
            self.data=self.data.drop(columns=self.data.columns[self.data.isna().any()])
            root.destroy()
        from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
        from sklearn.preprocessing import LabelEncoder

        
        def mf():
            from sklearn.experimental import enable_iterative_imputer
            from sklearn.impute import IterativeImputer

            

                        # One-hot encode with a unique separator to protect original column names
            df_dummy = pd.get_dummies(self.data, dummy_na=True, prefix_sep='___')

            # Impute missing values
            imputer = IterativeImputer(random_state=0)
            X_imputed = imputer.fit_transform(df_dummy.values)
            df = pd.DataFrame(X_imputed, columns=df_dummy.columns)

            # Remove _nan columns
            df = df.loc[:, ~df.columns.str.endswith('nan')]

            # Convert one-hot columns back to categorical
            numeric_cols = self.data.select_dtypes(include='number').columns
            one_hot_cols = [c for c in df.columns if c not in numeric_cols]

            # Group one-hot columns by original feature (everything before ___)
            from collections import defaultdict

            groups = defaultdict(list)
            for col in one_hot_cols:
                prefix = col.split('___')[0]
                groups[prefix].append(col)

            # Convert each group back to single categorical column
            for prefix, cols in groups.items():
                df[prefix] = df[cols].idxmax(axis=1).str.replace(prefix + '___', '', regex=False)
                df = df.drop(columns=cols)

            # Final clean DataFrame
            self.data = df


            root.destroy()

        root = tk.Tk()
        root.title("Image in Tkinter")

        # ---- main container ----
        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)

        # ---- left: image ----
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side="left", padx=10)

        image = Image.open("example.png").resize((200, 200))
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(left_frame, image=photo)
        label.image = photo   # keep reference
        label.pack()

        # ---- right: buttons ----
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="left", padx=20)

        tk.Button(right_frame, text="Mean Impute",command=mean_impute).pack(fill="x", pady=5)
        tk.Button(right_frame, text="Delete Missing Rows",command=dropna).pack(fill="x", pady=5)
        tk.Button(right_frame, text="Delete Missing Columns",command=dropnacolumns).pack(fill="x", pady=5)
        tk.Button(right_frame, text="Iterative Imputer",command=mf).pack(fill="x", pady=5)
        tk.Button(right_frame, text="Quit",command=root.destroy).pack(fill="x", pady=5)


        root.mainloop()


        
                

    def encode_categorical(self, col, mapping,poly=1):
        if mapping is None:
            return self.data
        df = self.data.copy()
        for p in range(poly):
            df[f"{col}_ordinal_{p}"] = df[col].map(mapping)**p

        

        return df
    def is_low_cardinality(self,series, max_unique=10):
        seen = set()

        for x in series:
            seen.add(x)
            if len(seen) > max_unique:
                return False  # high cardinality / continuous-ish
        
        if pd.to_numeric(pd.Series(list(seen)), errors="coerce").notna().all() or len(seen)==2:
            return False
        
        return True
    def select_items_gui(self,options,optionnames, title="Select Items"):
        selected = []

        def submit():
            nonlocal selected
            selected = [opt for opt, var in zip(options, vars_) if var.get()]
            root.destroy()

        root = tk.Tk()
        root.title(title)

        vars_ = []
        for opt,optionname in zip(options,optionnames):
            var = tk.BooleanVar(value=True)
            chk = ttk.Checkbutton(root, text=optionname, variable=var)
            chk.pack(anchor="w", padx=10)
            vars_.append(var)

        ttk.Button(root, text="Submit", command=submit).pack(pady=10)

        root.mainloop()
        return selected
    

    

    def assign_category_levels(self,name,
        categories,
        values=None,
        title="Assign Category Levels"
    ):
        """
        categories: list of strings
        values: list of allowed numeric assignments (default 1..len(categories))

        returns:
            dict {category: assigned_value or None}
            OR None if user cancels / treats as nominal
        """

        if values is None:
            values = list(range(len(categories) ))

        result = {}
        cancelled = False

        root = tk.Tk()
        root.title(title)

        frame = ttk.Frame(root, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text=name).grid(row=0, column=0, padx=5)
        ttk.Label(frame, text="Assigned Level").grid(row=0, column=1, padx=5)

        vars_ = {}

        for i, cat in enumerate(categories, start=1):
            ttk.Label(frame, text=cat).grid(row=i+1, column=0, sticky="w", padx=5)

            var = tk.StringVar(value="0")
            dropdown = ttk.Combobox(
                frame,
                textvariable=var,
                values=list(map(str, values)),
                width=10,
                state="readonly"
            )
            dropdown.grid(row=i+1, column=1, padx=5)

            vars_[cat] = var

        def submit():
            nonlocal result
            for cat, var in vars_.items():
                val = var.get()
                result[cat] = None if val == "Ignore" else int(val)
            root.destroy()

        def cancel():
            nonlocal cancelled
            cancelled = True
            root.destroy()

        button_frame = ttk.Frame(frame)
        button_frame.grid(
            row=len(categories) + 2,
            column=0,
            columnspan=3,
            pady=15
        )
        ttk.Label(button_frame, text="Add Poly Terms?").pack(side="left", padx=5)

        poly = tk.StringVar(value="1")
        dropdown = ttk.Combobox(
            button_frame,
            textvariable=poly,
            values=[str(x) for x in range(1,5)],
            width=10,
            state="readonly"
        )
        dropdown.pack(side="left", padx=5)

            
        ttk.Button(button_frame, text="Submit", command=submit).pack(side="left", padx=5)
        ttk.Button(
            button_frame,
            text="Cancel / Treat as Nominal",
            command=cancel
        ).pack(side="left", padx=5)

        root.mainloop()

        if cancelled:
            return None,None

        return result,int(poly.get())






            
