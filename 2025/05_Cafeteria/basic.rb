input_file = ARGV[0]

lines = File.readlines(input_file).map(&:strip)
line_break = lines.index('')

valid_id_ranges = lines[0..line_break-1].map do |line|
  line.split('-').map(&:to_i)
end

ids = lines[line_break+1..-1].map(&:to_i)

valid_id_count = 0
ids.each do |id|
  is_valid = false
  valid_id_ranges.each do |lower,upper|
    is_valid = (id >= lower and id <= upper)
    break if is_valid
  end
  if is_valid
    valid_id_count += 1
    next
  end
end

puts valid_id_count

