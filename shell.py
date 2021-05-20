def std_print_items( items ):
  for idx, data in enumerate( items, start=1 ):
    print( f'[ {idx} ]: {data}' )
  print( '[ X ]: Выйти' )

def std_read_item_from_items( header, items ):
  item = None
  while True:
    print( header )
    std_print_items( items )
    try:
      item = int( input( '> ' ) )
      if ( item < 1 or item > len( items ) ):
        print( 'Осуществляем выход...' )
        exit()
      else:
        return item - 1
    except ( ValueError ):
      print( "Неверный формат данных. Попробуйте еще раз..." )

def std_read_approximation_nodes_number():
  nodes_number = None
  while True:
    nodes_number = input( "Введите число узлов аппроксимации ( не менее 12 ): " )
    try:
      nodes_number = int( nodes_number )
      if ( nodes_number >= 1 ):
        break
      else:
        print( "Узлов аппроксимации должно быть не менее 12. Попробуйте еще раз..." )
    except ( ValueError ):
      print( "Неверный формат данных. Попробуйте еще раз..." )
  return nodes_number

def get_read_file_by_path():
  path = None
  while True:
    path = input( 'Введите путь до файла: ' )
    try:
      return open( path, 'r' )
    except ( FileNotFoundError ):
      print( f'Файл {path} не найден' )

def get_write_file_by_path():
  path = None
  while True:
    path = input( 'Введите путь до файла: ' )
    try:
      return open( path, 'w' )
    except ( Error ):
      print( 'Внутренняя ошибка' )
      exit()

def std_read_ipair( i ):
  xy = None
  while True:
    xy = input( f'[ {i + 1} ]: Введите узел ( x, y ): ' )
    try:
      x, y = xy.split( ' ', 2 )
      return ( float( x ), float( y ) )
    except ( ValueError ):
      print( "Неверный формат данных. Попробуйте еще раз..." )
    except ( IndexError ):
      print( "Неверный формат данных. Попробуйте еще раз..." )

def extract_nodes():
  # read the source of data
  input_item = std_read_item_from_items( 'Выберите источник данных:', [ 'Файл', 'Консоль' ] )
  input_file = None
  input_content = None
  # read file and content if file was chosen
  if input_item == 0:
    input_file = get_read_file_by_path()
    input_content = [ line for line in input_file ]
    input_file.close()

  # number of approximation nodes
  nodes_number = None
  if input_item == 1:
    nodes_number = std_read_approximation_nodes_number()
  else:
    try:
      nodes_number = int( input_content[ 0 ] )
    except ( ValueError ):
      print( f'Файл поврежден — не удалось распознать строку {input_content[0]}' )
      exit()

  # starting getting nodes itself
  print( f'Будет считано {nodes_number} узлов аппроксимации' )
  X = []
  Y = {}
  for i in range( nodes_number ):
    x = None
    y = None

    if input_item == 1:
      x, y = std_read_ipair( i )
    else:
      try:
        x, y = map( lambda numbers: float( numbers ), input_content[ i + 1 ].split( ' ', 2 ) )
      except ( ValueError ):
        print( f'Файл поврежден — не удалось распознать строку {input_content[ i + 1 ]}' )
        exit()
      except ( IndexError ):
        print( f'Файл поврежден — не удалось распознать строку {input_content[ i + 1 ]}' )
        exit()
    try:
      X.index( x )
    except ValueError:
      X.append( x )
    Y[ x ] = y
    print( f'Считан узел: ( {x}, {y} )' )
  return ( X, Y )