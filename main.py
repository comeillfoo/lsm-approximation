from shell import *
from approximation import *
from visualize import *

# global keys for methods
key_linear = methods()[ 0 ]
key_quadratic = methods()[ 1 ]
key_degree = methods()[ 2 ]
key_exponential = methods()[ 3 ]
key_logariphmic = methods()[ 4 ]

def main():
  try:
    X, Y = extract_nodes()


    # pearson correlation coefficient
    pearson = calculate_pearson_correlation( X, Y )


    # coefficients, lambdas and deviations
    coefficients = { method: coefficients_calculators()[ method ]( X, Y ) for method in methods() }
    functions = { method: lambda_generators()[ method ]( *coefficients[ method ] ) for method in methods() }
    deviations = [ calculate_deviation( functions[ method ], X, Y ) for method in methods() ]
    m_deviations = { methods()[ idx ]: deviations[ idx ] for idx in range( len( deviations ) ) }


    # get the source for output
    output_item = std_read_item_from_items( 'Выберите источник для записи результатов:', [ 'Файл', 'Консоль' ] )
    output_file = None

    # out the results
    if output_item == 0:
      output_file = get_write_file_by_path()
      for method in methods():
        output_file.write( format_out( method, coefficients[ method ], m_deviations[ method ], pearson ) )
      output_file.close()
    else:
      for method in methods():
        print( format_out( method, coefficients[ method ], m_deviations[ method ], pearson ) )


    # print out the best one
    best_method = methods()[ deviations.index( min( deviations ) ) ]
    print_best( best_method, coefficients[ best_method ], m_deviations[ best_method ], pearson )


    # drawing information
    formats = drawing_formats()
    labels = drawing_labels()
    drawing_functions = [ { 'f': functions[ method ], 'fmt': formats[ method ], 'lbl': labels[ method ] } for method in methods() ]


    # set drawing format for the best one to the bold
    drawing_functions[ deviations.index( min( deviations ) ) ][ 'fmt' ] = 'r-'


    # draw all
    drawall( X, Y, drawing_functions )
  except ( KeyboardInterrupt ):
    print( '\nЗавершение программы...' )


if ( __name__ == "__main__" ):
  main()