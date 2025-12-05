input_file = ARGV[0]

lines = File.readlines(input_file).map(&:strip)
line_break = lines.index('')

valid_id_ranges = lines[0..line_break-1].map do |line|
  line.split('-').map(&:to_i)
end.sort

valid_ids_count = 0

l0, u0 = valid_id_ranges[0]
valid_id_ranges.each do |l,u|
  if u0 < l
    valid_ids_count += u0 - l0 + 1
    l0, u0 = [l, u]
  elsif u > u0
    u0 = u
  end
end
valid_ids_count += u0 - l0 + 1

puts valid_ids_count
