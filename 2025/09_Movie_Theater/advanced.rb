input_file = ARGV[0]

tiles = File.readlines(input_file).map do |line|
  line.strip.split(',').map(&:to_i)
end

# The tiles are given in a sequence
# We can store edges by taking iterating over tiles 2 at a time
x_edges = [] # Vertical edges
y_edges = [] # Horizontal edges
tiles.each_with_index do |(x0,y0), i0|
  x1,y1 = tiles[(i0+1)%tiles.count]
  
  edge = []
  if x1 == x0
    x_edges << [x0, [y0,y1].sort]
  else
    y_edges << [[x0,x1].sort, y0]
  end
  edge
end

puts "+ EDGES +---------------"
puts x_edges.map(&:inspect)
puts y_edges.map(&:inspect)

max_area = -1
tiles.each_with_index do |(x0, y0), i0|
  tiles[i0+1..-1].each_with_index do |(x1, y1), i1|
    xs0,xs1 = [x0, x1].sort
    ys0,ys1 = [y0, y1].sort
    crosses_edge = false

    x_edges.each do |xe, (ye0, ye1)|
      next if xe < xs0 or xe > xs1
      crosses_edge = ((ye0 <= ys0) and (ys0 <= ye1)) or
                     ((ye0 <= ys1) and (ys1 <= ye1))
      next if crosses_edge
    end
    next if crosses_edge

    y_edges.each do |(xe0, xe1), ye|
      next if ye < ys0 or ye > ys1
      crosses_edge = ((xe0 <= xs0) and (xs0 <= xe1)) or
                     ((xe0 <= xs1) and (xs1 <= xe1))
      next if crosses_edge
    end
    next if crosses_edge
    area = ((x0-x1).abs + 1) * ((y0-y1).abs + 1)
    max_area = area if area > max_area
  end
end

puts "+ RESULT +-----------------"
puts max_area
