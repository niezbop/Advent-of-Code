input_file = ARGV[0]
debug = ARGV.include?('-d') or ARGV.include?('--debug')

map = File.readlines(input_file).map(&:strip).map(&:chars)

NEIGHBOUR_VECTORS = [
  [0, 1], # Right
  [1, 1], # Bottom right
  [1, 0], # Bottom
  [1, -1], # Bottom left
  [0, -1], # Left
  [-1, -1], # Top left
  [-1, 0], # Top
  [-1, 1] # Top right
].freeze

ROWS = map.length
COLUMNS = map[0].length

def neighbours(map, i, j)
  neighbours = []

  NEIGHBOUR_VECTORS.each do |u,v|
    next if i+u < 0
    next if i+u >= ROWS
    next if j+v < 0
    next if j+v >= COLUMNS
    yield map[i+u][j+v] if block_given?
    neighbours << map[i+u][j+v]
  end

  return neighbours
end

accessible_rolls = 0
debug_map = []

map.each_with_index do |row, i|
  debug_row = row.dup
  row.each_with_index do |char, j|
    next unless char == '@'

    neighbouring_rolls = 0
    neighbours(map, i, j) do |other_char|
      neighbouring_rolls += 1 if other_char == '@'
    end

    if neighbouring_rolls < 4
      accessible_rolls += 1
      debug_row[j] = 'x'
    end
  end
  debug_map << debug_row
end

if debug
  debug_map.each do |row|
    puts row.join('')
  end
end

puts accessible_rolls
