import pickle
from tqdm import tqdm

def buffered_writer(iterable, fp_write, *args, format="pickle", buffer_size=1024):
    """:param iterable: an iterable"""
    
    def _writer(batch, f):
        if format == "pickle":
            pickle.dump(batch, f, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            ...
    
    with open(fp_write, "wb") as f, tqdm(desc="Writing to file") as pbar:
        batch = []

        for item in iterable:
            
            batch.append(item)
            pbar.update(1)

            if len(batch) >= buffer_size:
                _writer(batch, f)
                batch.clear()

        if batch:
            _writer(batch, f)