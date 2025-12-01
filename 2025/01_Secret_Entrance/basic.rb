input_file = ARGV[0]

lines = File.readlines(input_file)

dial_at_zero = 0
dial = 50

lines.each do |line|
  next if line.empty?

  char = line.slice!(0)
  value = line.strip.to_i

  if char == 'L'
    dial -= value
  elsif char == 'R'
    dial += value
  else
    raise ArgumentError, "Character #{char} not recognized"
  end

  dial = dial % 100
  dial_at_zero += 1 if dial == 0
end

puts "Dial reached zero #{dial_at_zero} times"

