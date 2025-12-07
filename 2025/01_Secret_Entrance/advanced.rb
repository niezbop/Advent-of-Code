input_file = ARGV[0]

lines = File.readlines(input_file)

dial_at_zero = 0
dial = 50

lines.each do |line|
  next if line.empty?

  char = line.slice!(0)
  value = line.strip.to_i

  start_at_zero = dial.zero?

  if char == 'L'
    dial -= value
  elsif char == 'R'
    dial += value
  else
    raise ArgumentError, "Character #{char} not recognized"
  end

  q,r = dial.divmod(100)

  if char == 'L'
    dial_at_zero -= 1 if start_at_zero  # The first iteration doesn't cross the threshold
    dial_at_zero += 1 if r == 0         # Because it was counted there
  end
  dial_at_zero += q.abs
  dial = r
end

puts "Dial reached zero #{dial_at_zero} times"

