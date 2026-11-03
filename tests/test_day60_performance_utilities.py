import pytest
from utils.performance_benchmark import TTLCache, process_in_batches, benchmark_callable

def test_batch_processing_preserves_order():
    assert process_in_batches([1,2,3,4,5],lambda x:x*x,2)==[1,4,9,16,25]

def test_empty_batch():
    assert process_in_batches([],str,3)==[]

@pytest.mark.parametrize("size",[0,-1,True])
def test_invalid_batch_size(size):
    with pytest.raises(ValueError): process_in_batches([1],str,size)

def test_cache_get_set_and_lru():
    cache=TTLCache(max_items=2,ttl_seconds=60)
    cache.set("a",1); cache.set("b",2)
    assert cache.get("a")==1
    cache.set("c",3)
    assert cache.get("b") is None and cache.get("c")==3

def test_cache_expiry():
    now=[0.0]
    cache=TTLCache(ttl_seconds=2,clock=lambda:now[0])
    cache.set("key","value"); now[0]=3
    assert cache.get("key") is None

def test_benchmark_shape():
    result=benchmark_callable(lambda: sum(range(10)),iterations=3)
    assert result["iterations"]==3 and result["max_ms"]>=0
    assert "Local microbenchmark" in result["measurement_note"]

def test_invalid_iterations():
    with pytest.raises(ValueError): benchmark_callable(lambda:None,0)
