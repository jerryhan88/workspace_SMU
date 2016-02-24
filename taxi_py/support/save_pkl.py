from __future__ import division
# from os.path import getmtime, isfile
import pickle

# def pickling(path, _objects):
#     pkl_path = path + '.pkl'
#     # read pickled file if available.
#     if isfile(pkl_path) and getmtime(path) < getmtime(pkl_path):
#         with open(pkl_path, 'rb') as fp:
#             return pickle.load(fp)
#     # pickle.
#     with open(pkl_path, 'wb') as fp:
#         pickle.dump(_objects, fp)
#     return IS, NS, LS

def save_pickle_file(path, _objects):
    pkl_path = path + '.pkl'
    with open(pkl_path, 'wb') as fp:
        pickle.dump(_objects, fp)
        
def load_picle_file(path):
    with open(path, 'rb') as fp:
        return pickle.load(fp)
    
    