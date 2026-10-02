"""Descriptive feature shift only; not an automated production drift alarm."""
from pathlib import Path
import pandas as pd
if __name__=='__main__':
    x=pd.read_csv('data/features.csv');a=int(len(x)*.6);b=int(len(x)*.8)
    ref=x.iloc[:a];current=x.iloc[b:]
    out=pd.DataFrame({'training_mean':ref.mean(),'holdout_mean':current.mean(),'training_std':ref.std()})
    out['absolute_standardized_mean_shift']=(out.holdout_mean-out.training_mean).abs()/out.training_std.replace(0,float('nan'))
    out.index.name='feature';out.to_csv('reports/feature_shift.csv');print(out.to_string())
