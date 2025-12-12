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
    return (self.left <= x and self.right >= x and
            self.top <= y and self.bottom >= y)
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
  board = BOARD.dup
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

max_area = -1
best_rectangle = nil

rectangles.each_with_index do |r0, i0|
  next if r0.area <= max_area
  next if rectangles.each_with_index.any? do|r1,i1|
    next false if i0 == i1

    r0.overlaps?(r1) and !(r0.is_inside?(r1) or r1.is_inside?(r0))
  end
  max_area = r0.area
  best_rectangle = r0
end

print_board({best_rectangle => :green})

puts max_area
