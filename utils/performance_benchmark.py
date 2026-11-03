"""Dependency-free batch, cache and latency measurement utilities."""
from collections import OrderedDict
from statistics import mean, median
from time import perf_counter
from threading import RLock

class TTLCache:
    def __init__(self, max_items=256, ttl_seconds=60.0, clock=perf_counter):
        if isinstance(max_items,bool) or not isinstance(max_items,int) or max_items < 1:
            raise ValueError("max_items must be a positive integer")
        if isinstance(ttl_seconds,bool) or not isinstance(ttl_seconds,(int,float)) or ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        self.max_items=max_items; self.ttl=float(ttl_seconds); self.clock=clock
        self._items=OrderedDict(); self._lock=RLock()

    def get(self,key,default=None):
        with self._lock:
            item=self._items.get(key)
            if item is None: return default
            expires,value=item
            if self.clock() >= expires:
                del self._items[key]; return default
            self._items.move_to_end(key); return value

    def set(self,key,value):
        with self._lock:
            self._items[key]=(self.clock()+self.ttl,value)
            self._items.move_to_end(key)
            while len(self._items)>self.max_items: self._items.popitem(last=False)

    def clear(self):
        with self._lock: self._items.clear()

def process_in_batches(items, processor, batch_size=32):
    if not isinstance(items,(list,tuple)): raise TypeError("items must be a list or tuple")
    if not callable(processor): raise TypeError("processor must be callable")
    if isinstance(batch_size,bool) or not isinstance(batch_size,int) or batch_size<1:
        raise ValueError("batch_size must be a positive integer")
    output=[]
    for start in range(0,len(items),batch_size):
        batch=items[start:start+batch_size]
        output.extend(processor(item) for item in batch)
    return output

def benchmark_callable(operation, iterations=10):
    if not callable(operation): raise TypeError("operation must be callable")
    if isinstance(iterations,bool) or not isinstance(iterations,int) or iterations<1:
        raise ValueError("iterations must be a positive integer")
    samples=[]
    for _ in range(iterations):
        start=perf_counter(); operation(); samples.append((perf_counter()-start)*1000)
    ordered=sorted(samples)
    p95=ordered[min(len(ordered)-1, int(.95*(len(ordered)-1)))]
    return {"iterations":iterations,"mean_ms":round(mean(samples),4),
            "median_ms":round(median(samples),4),"p95_ms":round(p95,4),
            "min_ms":round(min(samples),4),"max_ms":round(max(samples),4),
            "measurement_note":"Local microbenchmark only; not a production load-test result."}
