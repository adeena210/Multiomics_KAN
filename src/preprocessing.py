# %%
import scanpy as sc
import pandas as pd
import torch
import numpy as np
from torch.utils.data import DataLoader, TensorDataset


# %%
def preprocess(input_path, meta_path, batch_size=64):
    adata = sc.read_text(input_path)
    meta = pd.read_csv(meta_path, sep="\t")
    adata.var = meta

    # normalize cells to have the same total counts
    sc.pp.normalize_total(adata, target_sum=1e4)
    # logarithmize data
    sc.pp.log1p(adata)
    sc.pp.highly_variable_genes(adata, n_top_genes=2000)
    adata = adata[:, adata.var['highly_variable']]
    # unit variance + zero mean
    sc.pp.scale(adata)

    X = adata.X.toarray() if not isinstance(adata.X, np.ndarray) else adata.X
    X_tensor = torch.tensor(X, dtype=torch.float32)

    dataset = TensorDataset(X_tensor)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    return dataloader, X_tensor.shape[1]
