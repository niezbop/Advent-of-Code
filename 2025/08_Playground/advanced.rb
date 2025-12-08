input_file = ARGV[0]

coordinates = File.readlines(input_file).map do |line|
  line.strip.split(',').map(&:to_i)
end

distances = Hash.new
circuits = Array.new

coordinates.each_with_index do |(x0, y0, z0), i0|
  circuits << [i0]
  coordinates.each_with_index do |(x1, y1, z1), i1|
    next if i0 >= i1
    distance = Math.sqrt(
      (x0-x1)**2 +
      (y0-y1)**2 +
      (z0-z1)**2
    )
    distances[[i0,i1]] = distance
  end
end

result = -1
distances.sort_by {|_, d| d}.each do |(i0,i1), _|
  c0 = circuits.find {|c| c.include?(i0) }
  next if c0.include?(i1)

  c1 = circuits.find {|c| c.include?(i1) }
  circuits.delete(c0)
  circuits.delete(c1)

  circuits << c0 + c1

  if circuits.size == 1
    result = coordinates[i0][0] * coordinates[i1][0]
    break
  end
end

puts result
