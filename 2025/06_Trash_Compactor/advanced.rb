input_file = ARGV[0]

lines = File.readlines(input_file)
operands = lines[-1].split.map(&:to_sym)

total = 0
column_index = 0
numbers = []
lines[0].size.times do |i|
  characters = lines[0..-2].map {|l| l[i] }.reject {|c| c.strip.empty? }
  if characters.none?
    total += numbers.reduce(operands[column_index])
    column_index += 1
    numbers = []
  else
    numbers << characters.join.to_i 
  end
end

puts total
