import matplotlib as mat
import matplotlib.pyplot as plt
import numpy as np

def draw_array( X, Y ):
  plt.plot( X, [ y for y in Y.values() ], 'ro', label='y = f( x )' )

def draw_interval( a, b, f, fmt, lbl ):
  X = np.arange( a - 2, b + 2, 1e-3 )
  y = []
  for x in X:
    try:
      y.append( f( x ) )
    except ValueError:
      y.append( None )
  plt.plot( X, y, fmt, label=lbl )

def drawall( X, Y, funs ):
  a = min( X )
  b = max( X )
  plt.grid( True, 'both', 'both' )
  plt.axis( [ a, b, min( Y.values() ), max( Y.values() ) ] )
  for fun in funs:
    draw_interval( a, b, fun[ 'f' ], fun[ 'fmt' ], fun[ 'lbl' ] )
  draw_array( X, Y )
  plt.ylabel( 'y', horizontalalignment='right', y=1.05, rotation=0 )
  plt.xlabel( 'x', horizontalalignment='right', x=1.05 )
  plt.legend()
  plt.show()