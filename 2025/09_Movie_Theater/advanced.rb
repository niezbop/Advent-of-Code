require 'colored2'
input_file = ARGV[0]
visualize = ARGV.include?('-v') or ARGV.include?('--visualize')

tiles = File.readlines(input_file).map do |line|
  line.strip.split(',').map(&:to_i)
end

class Rectangle
  attr_accessor :x0, :y0, :x1, :y1

  def initialize(x0, y0, x1, y1)
    self.x0 = x0
    self.y0 = y0
    self.x1 = x1
    self.y1 = y1
  end

  def top; [y0,y1].min; end
  def bottom; [y0,y1].max; end
  def left; [x0,x1].min; end
  def right; [x0, x1].max; end

  def area; ((x0-x1).abs + 1) * ((y0-y1) + 1).abs; end

  def contains?(x,y)
    return (self.left < x and self.right > x and
            self.top < y and self.bottom > y)
  end

  def is_inside?(other)
    return (self.left >= other.left and
            self.right <= other.right and
            self.top >= other.top and
            self.bottom <= other.bottom)
  end

  def overlaps?(other)
    return !(self.left >= other.right or
             self.right <= other.left or
             self.top >= other.bottom or
             self.bottom <= other.top)

  end

  def visualize
    digit_size = [x0,y0,x1,y1].max.to_s.size
    format = "%0#{digit_size}d"
    puts " +---- #{format % top} ----+"
    puts ' |' + ' ' * (digit_size + 10) + '|'
    puts format % left + ' ' * 12 + format % right
    puts ' |' + ' ' * (digit_size + 10) + '|'
    puts " +---- #{format % bottom} ----+"
  end
end

X_MAX = tiles.map(&:first).sort.last.freeze
Y_MAX = tiles.map(&:last).sort.last.freeze
BOARD = (0..Y_MAX).map {|y| (0..X_MAX).map {|x| '.' }}
tiles.each_with_index do |(x0,y0), i|
  x1,y1 = tiles[(i+1)%tiles.size]
  BOARD[y0][x0] = 'O'
  if x1 == x0
    y_min,y_max = [y0,y1].sort
    (y_min+1..y_max-1).each {|y| BOARD[y][x0] = '#'}
  else
    x_min,x_max = [x0,x1].sort
    (x_min+1..x_max-1).each {|x| BOARD[y0][x] = '#'}
  end
end

def print_board(rectangle_colors = {}, refresh = false)
  board = []
  BOARD.each {|row| board << row.dup }
  rectangle_colors.each do |rectangle, color|
    (rectangle.left..rectangle.right).each do |x|
      (rectangle.top..rectangle.bottom).each do |y|
        board[y][x] = board[y][x].send(color)
      end
    end
  end
  puts board.map(&:join).join("\n")
end

rectangles = tiles.each_with_index.map do |(x0, y0), i|
  tiles[i+1..-1].map do |x1, y1|
    Rectangle.new(x0,y0, x1,y1)
  end
end.flatten

edges = tiles.each_with_index.map do |tile, i|
  next_tile = tiles[(i+1)%tiles.size]
  [tile, next_tile]
end

max_area = -1
best_rectangle = nil

rectangles.each_with_index do |r|
  next if r.area <= max_area
  next if edges.any? do |(x0,y0), (x1,y1)|
    if x0 == x1
      y_min, y_max = [y0, y1].sort
      next false if x0 <= r.left or x0 >= r.right
      next ((y_min <= r.top and y_max > r.top) or
            (y_min < r.bottom and y_max >= r.bottom))
    else
      x_min, x_max = [x0, x1].sort
      next false if y0 <= r.top or y0 >= r.bottom
      next ((x_min <= r.left and x_max > r.left) or
            (x_min < r.right and x_max >= r.right))
    end
  end
  max_area = r.area
  best_rectangle = r
end

puts max_area
