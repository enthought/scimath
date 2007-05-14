
from enthought.interpolate import *

def main():
    from enthought.util.numerix import arange, ones
    import time
    N = 3000.
    x = arange(N)
    y = arange(N)
    new_x = arange(N)+0.5
    t1 = time.clock()
    new_y = linear(x, y, new_x)
    t2 = time.clock()
    print '1d interp (sec):', t2 - t1
    print new_y[:5]

    N = 3000.
    x = arange(N)
    y = arange(N)
    new_x = arange(N)+0.5
    try:
        import log
    except ImportError, msg:
        print msg
        log = None
    if log is not None:
        lg = log.Log(x, index=y)
        lg2 = lg.sample_at(new_x)
        t1 = time.clock()
        lg2 = lg.sample_at(new_x)
        t2 = time.clock()
        print 'log.sample_at (sec):', t2 - t1
        print lg2.data[:5]
        from enthought.util.profiler import run
        #run("lg2 = lg.sample_at(new_x)")

    new_x = arange(N/2)*2
    t1 = time.clock()
    new_y = block_average_above(x, y, new_x)
    t2 = time.clock()
    print '1d block_average_above (sec):', t2 - t1
    print new_y[:5]
    
    N = 3000.
    x = arange(N)
    y = ones((100,N)) * arange(N)
    new_x = arange(N)+0.5
    t1 = time.clock()
    new_y = linear(x, y, new_x)
    t2 = time.clock()
    print 'fast interpolate (sec):', t2 - t1
    print new_y[:5,:5]

    import scipy
    N = 3000.
    x = arange(N)
    y = ones((100, N)) * arange(N)
    new_x = arange(N)
    t1 = time.clock()
    interp = scipy.interpolate.interp1d(x, y)
    new_y = interp(new_x)
    t2 = time.clock()
    print 'scipy interp1d (sec):', t2 - t1
    print new_y[:5,:5]

if __name__ == '__main__':
    main()
