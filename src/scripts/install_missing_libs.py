# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: altair-saver-python310
#     language: python
#     name: altair-saver-python310
# ---

# %% [markdown]
# This is for installing and capturing missing libraries.

# %% [markdown]
# The following conda install executed outside of a jupyter lab session can update the kernel being used by a jupyter session, making the missing lib import'able.
#
# The switch -c conda-forge makes the difference of avoiding version conflicts.
#
# !conda install -y -c conda-forge matplotlib 
# took more 10 minutes to complete. I wish there is a faster approach.

# %% [markdown]
# Using the following of pip is much faster. 
#
# But after executing it inside the jupyter session, the kernel used by the notebook needs to be restarted to take effect.

# %% jupyter={"outputs_hidden": true} tags=[]
import sys
# !{sys.executable} -m pip install --user seaborn

# %%

# %% jupyter={"outputs_hidden": true} tags=[]
# !conda install -y -c conda-forge matplotlib # It does have effect, sklearn still cannot be imported afeter the install and restarting the kernel

# %%
import sys
# !{sys.executable} -m pip install --user scikit-learn # Note, the one to install is scikit-learn, not the one to be imported!


# %%
# !conda install -y -c conda-forge sklearn # Indeed, this is much slower than pip install above.

# %% [markdown]
# Following this to install pytorch: https://pytorch.org/get-started/locally/#windows-pip

# %%
import sys
# !{sys.executable} -m pip install --user torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

# %%
# !ls ../../

# %%
# !conda list -e > ../../requirements-for-conda.txt

# %%
# !pip list --format=freeze > ../../requirements-with-pip.txt

# %%
conda create -y -n ac-mointor python=3.10
conda activate ac-mointor
pip3 install -r ./requirements-with-pip-doctored.txt
