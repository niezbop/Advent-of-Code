input_file = ARGV[0]
visualize_output = ARGV.include?('-v') or ARGV.include?('--verbose')

lines = File.readlines(input_file).map(&:strip)

class Shape
  attr_accessor :raw

  def initialize(raw = [])
    self.raw = raw
  end

  def <<(row)
    raise ArgumentError, "Mismatching row width" if !self.width.nil? and row.size != self.width
    self.raw << row
  end

  def width
    return nil if raw.empty?
    return raw[0].size
  end

  def length
    return nil if raw.empty?
    return raw.size
  end

  def occupied_tiles
    tiles = []
    raw.each_with_index do |row, i|
      row.each_with_index do |char, j|
        tiles << [j,i] if char == '#'
      end
    end
    return tiles
  end

  def footprint
    return occupied_tiles.count
  end

  def horizontal_flip
    return Shape.new(raw.reverse)
  end

  def vertical_flip
    return Shape.new(raw.map(&:reverse))
  end

  # Clockwise
  def rotate(by_90_increment = 1)
    by_90_increment = by_90_increment % 4
    return self if by_90_increment.zero?
    if by_90_increment == 1
      return Shape.new(raw.transpose.map(&:reverse))
    else
      return self.rotate.rotate(by_90_increment - 1)
    end
  end

  def permutations
    return [
      (0..3).map {|i| self.rotate(i)},
      (0..3).map {|i| self.horizontal_flip.rotate(i)}, # horizontal_flip + 180° = vertical_flip
    ].flatten
  end

  def visualize
    return raw.map {|row| row.join }.join("\n")
  end
end

shapes = []
regions = []

current_shape_index = nil
lines.each do |line|
  if line.empty?
    current_shape_index = nil 
  elsif current_shape_index != nil
    shapes[current_shape_index] << line.chars
  elsif line.start_with?(/\d+:/)
    current_shape_index = line.split(':')[0].to_i
    shapes[current_shape_index] = Shape.new
  else
    dimensions, indices = line.split(': ')
    dimensions = dimensions.split('x').map(&:to_i)
    indices = indices.split(' ').map(&:to_i)
    regions << {
      width: dimensions[0], 
      length: dimensions[1],
      shapes: indices.each_with_index.map {|count, index| [shapes[index]] * count }.flatten
    }
  end
end

class Board
  def initialize(width, length)
    self.inner = length.times.map { width.times.map { nil }}
  end

  def [](x,y)
    return inner[y][x]
  end

  def []=(x,y, value)
    inner[y][x] = value
  end

  def tile_positions
    return width.times.map do |x|
      length.times.map do |y|
        yield [x,y] if block_given?
        [x,y]
      end
    end.flatten(1)
  end

  def tiles
    tile_positions.map do |x,y|
      yield self[x,y] if block_given?
      self[x,y]
    end
  end

  def dup
    board = Board.new(self.width, self.length)
    self.tile_positions do |x,y|
      board[x,y] = self[x,y]
    end
    return board
  end

  def width; inner[0].size; end
  def length; inner.size; end

  def visualize
    return inner.map { |row| row.map {|c| c.nil? ? '.' : c }.join }.join("\n")
  end

  private attr_accessor :inner
end

def region_fits?(visualize_board = false, width:, length:, shapes:)
  shapes_width = shapes[0].width
  shapes_length = shapes[0].length
  return true if (width / shapes_width) * (length/shapes_length) >= shapes.count
  return false if shapes.map(&:footprint).sum > width * length
  return recursive_region_fits?(
    Board.new(width, length),
    shapes.sort_by(&:footprint).reverse,
    visualize_board)
end

def recursive_region_fits?(board, shapes, visualize_board)
  positions = board.tile_positions
  shapes.each_with_index do |shape, index|
    next if shape.nil? # Already fit
    shape.permutations.each do |permutation|
      positions.each do |x,y|
        shape_fits = permutation.occupied_tiles.all? do |u,v|
          next false if x+u >= board.width or y+v >= board.length
          board[x+u,y+v].nil?
        end
        next unless shape_fits
        remaining_shapes = shapes.dup
        remaining_shapes[index] = nil
        new_board = board.dup
        permutation.occupied_tiles.each {|u,v| new_board[x+u,y+v] = index}
        if remaining_shapes.compact.empty?
          puts new_board.visualize if visualize_board
          return true
        end
        return true if recursive_region_fits?(new_board, remaining_shapes, visualize_board)
      end
    end
  end
  return false
end

regions_that_fit = regions.select do |region|
  # region[:shapes].map(&:footprint).sum <= region[:width] * region[:length]
  region_fits?(visualize_output, **region)
end.count
puts regions_that_fit
