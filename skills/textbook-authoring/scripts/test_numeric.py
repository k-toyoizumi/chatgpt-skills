#!/usr/bin/env python3
"""Verify the toy QKV example shown in the chapter, independently in NumPy.
Run torch example too when PyTorch is available. Never claim a pass for an unavailable library.
"""
import math
import numpy as np
from pathlib import Path
import re
Q = np.array([[1., 0.], [0., 1.], [1., 1.]])
K = Q.copy()
V = np.array([[2., 0.], [0., 2.], [2., 2.]])
S=Q @ K.T/math.sqrt(Q.shape[-1]); P=np.exp(S-S.max(axis=-1,keepdims=True)); A=P/P.sum(axis=-1,keepdims=True); Z=A@V
assert np.allclose(A.sum(axis=-1),1.0,atol=1e-12)
assert np.allclose(A[0], [.40111209,.19777581,.40111209],atol=1e-5)
assert np.allclose(Z[0], [1.60444836,1.19777581],atol=1e-5)
mask=np.triu(np.ones((3,3),dtype=bool), k=1)
S2=S.copy();S2[mask]=-np.inf
p2=np.exp(S2-S2.max(axis=-1,keepdims=True));A2=p2/p2.sum(axis=-1,keepdims=True)
assert np.all(A2[mask]==0.) and np.allclose(A2.sum(axis=-1),1.0)
svg=(Path(__file__).resolve().parents[1]/'assets/quarto-book/figures/03-weight-matrix.svg').read_text()
# The chapter diagram must agree to 3 decimal places with actually computed values.
for row in A:
    for v in row:
        assert f'{v:.3f}' in svg, f'Figure missing weight {v:.3f}'
print('PASS: NumPy QKV, softmax axis, weighted Value, causal mask, SVG heatmap')
try:
    import torch
except ImportError:
    print('NOT RUN: PyTorch unavailable')
else:
    q=torch.tensor(Q,dtype=torch.float32); k=torch.tensor(K,dtype=torch.float32); v=torch.tensor(V,dtype=torch.float32)
    scores = q @ k.T / math.sqrt(q.shape[-1])
    weights=torch.softmax(scores,dim=-1); z=weights@v
    assert torch.allclose(weights.sum(dim=-1),torch.ones(3),atol=1e-6)
    assert np.allclose(weights.numpy(),A,atol=1e-6)
    assert np.allclose(z.numpy(),Z,atol=1e-6)
    print('PASS: PyTorch matches NumPy numerical example')
