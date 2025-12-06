input_file = ARGV[0]

lines = File.readlines(input_file).map(&:strip).map(&:split)

total = 0
(0..lines[0].size-1).each do |i|
  operand = lines[-1][i].to_sym
  total += lines[0..-2].map { |row| row[i].to_i }.reduce(operand)
end

puts total
