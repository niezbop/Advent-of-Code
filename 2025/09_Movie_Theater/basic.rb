input_file = ARGV[0]

tiles = File.readlines(input_file).map do |line|
  line.strip.split(',').map(&:to_i)
end

max_area = -1
tiles.each_with_index do |(x0, y0), i0|
  tiles[i0+1..-1].each do |x1, y1|
    area = ((x0-x1).abs + 1) * ((y0-y1).abs + 1)
    max_area = area if area > max_area
  end
end

puts max_area
