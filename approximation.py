from math import log, exp, sqrt
import numpy
from statistics import mean

key_linear = 'linear'
key_quadratic = 'quadratic'
key_degree = 'degree'
key_exponential = 'exponential'
key_logariphmic = 'logariphmic'

def format_out( method, coefficients, deviation, pearson = 0 ):
  if ( method == key_quadratic ):
    return "{} {} {} {}\n".format( *coefficients, deviation )
  elif ( method == key_linear ):
    return "{} {} {} {}\n".format( *coefficients, deviation, pearson )
  else:
    return "{} {} {}\n".format( *coefficients, deviation )

def print_best( method, coefficients, deviation, pearson = 0 ):
  print( f'Лучшая аппроксимация: [ {method} ]' )
  print( format_out( method, coefficients, deviation, pearson ) )

def methods():
  return [ key_linear, key_quadratic, key_degree, key_exponential, key_logariphmic, ]

def calculate_deviation( f, X, y ):
  sum = 0
  for x in X:
    sum += ( f( x ) - y[ x ] )**2
  return sum

def calculate_pearson_correlation( X, Y ):
  _x = mean( X ) 
  _y = mean( Y.values() )
  SX_MXY_MY = 0
  SX_MXX_MX = 0
  SY_MYY_MY = 0
  for x in X:
    SX_MXY_MY += ( x - _x ) * ( Y[ x ] - _y )
    SX_MXX_MX += ( x - _x ) * ( x - _x )
    SY_MYY_MY += ( Y[ x ] - _y ) * ( Y[ x ] - _y )
  return SX_MXY_MY / sqrt( SX_MXX_MX * SY_MYY_MY )

# bunch functions calculating coefficients
def calculate_linear_approximation_coefficients( X, y ):
  n = len( X )
  SX = sum( X )
  SXX = sum( [ x**2 for x in X ] )
  SY = sum( y.values() )
  SXY = 0
  for x in X:
    SXY += x * y[ x ]
  d = SXX * n - SX**2
  d1 = SXY * n - SX * SY
  d2 = SXX * SY - SX * SXY
  return ( d1 / d, d2 / d )

def calculate_quadratic_approximation_coefficients( X, y ):
  n = len( X )
  SX = sum( X )
  SY = sum( y.values() )
  SXX = sum( [ x**2 for x in X ] )
  SXXX = sum( [ x**3 for x in X ] )
  SXXXX = sum( [ x**4 for x in X ] )
  SXY = 0
  SXXY = 0
  for x in X:
    SXY += x * y[ x ]
    SXXY += x**2 * y[ x ]
  A = numpy.array( [ [ n, SX, SXX ], [ SX, SXX, SXXX ], [ SXX, SXXX, SXXXX ] ] )
  B = numpy.array( [ SY, SXY, SXXY ] )
  X = numpy.linalg.inv( A ).dot( B )
  return tuple( X )

def calculate_exponential_approximation_coefficients( X, y ): 
  logY = {}
  for x in X:
    if y[ x ] > 0:
      logY[ x ] = log( y[ x ] )
    else:
      print( f'Warning: значение функции отрицательно в точке, узел ( {x}, {y[ x ]} ) будет пропущен' )
      logY[ x ] = 0

  B, A = calculate_linear_approximation_coefficients( X, logY )
  return ( exp( A ), B )

def calculate_degree_approximation_coefficients( X, y ):
  # build logariphmed X
  logX = []
  for x in X:
    if y[ x ] > 0 and x > 0:
      logX.append( log( x ) )
    else:
      print( f'Warning: узел ( {x}, {y[ x ]} ) будет пропущен' )

  # build logariphmed Y
  logY = {}
  for x in X:
    if y[ x ] > 0 and x > 0:
      logY[ log( x ) ] = log( y[ x ] )
    else:
      print( f'Warning: узел ( {x}, {y[ x ]} ) будет пропущен' )  

  B, A = calculate_linear_approximation_coefficients( logX, logY )
  return ( exp( A ), B )

def calculate_logariphmic_approximation_coefficients( X, y ):
  # build logariphmed X
  logX = []
  Y = {}
  for x in X:
    if x > 0:
      logX.append( log( x ) )
      Y[ log( x ) ] = y[ x ]
    else:
      print( f'Warning: узел ( {x}, {y[ x ]} ) будет пропущен' )

  A, B = calculate_linear_approximation_coefficients( logX, Y )
  return ( A, B )

def coefficients_calculators():
  return {
    key_linear: calculate_linear_approximation_coefficients,
    key_quadratic: calculate_quadratic_approximation_coefficients,
    key_degree: calculate_degree_approximation_coefficients,
    key_exponential: calculate_exponential_approximation_coefficients,
    key_logariphmic: calculate_logariphmic_approximation_coefficients,
  }

def linear_lambda_generator( A, B ):
  return lambda x: A * x + B

def degree_lambda_generator( A, B ):
  return lambda x: A * x**B

def exponent_lambda_generator( A, B ):
  return lambda x: A * exp( B * x )

def logariphmic_lambda_generator( A, B ):
  return lambda x: A * log( x ) + B

def quadratic_lambda_generator( A0, A1, A2 ):
  return lambda x: A0 + A1 * x + A2 * x * x

def lambda_generators():
  return {
    key_linear: linear_lambda_generator,
    key_quadratic: quadratic_lambda_generator,
    key_degree: degree_lambda_generator,
    key_exponential: exponent_lambda_generator,
    key_logariphmic: logariphmic_lambda_generator,
  }

def drawing_formats():
  return { key_linear: 'r--', key_quadratic: 'b--', key_degree: 'y--', key_exponential: 'g--', key_logariphmic: 'c--', }

def drawing_labels():
  return { key_linear: 'y = ax + b', key_quadratic: 'a0 + a1 x + a2 x^2', key_degree: 'y = ax^b', key_exponential: 'y = ae^bx', key_logariphmic: 'y = aln(x) + b', }
