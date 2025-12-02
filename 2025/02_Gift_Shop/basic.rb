input_file = ARGV[0]

input = File.read(input_file)

ranges = input.split(',')

invalid_ids_total = 0

def is_id_valid?(id)
  characters = id.to_s
  digits_count = characters.length
  return true if digits_count.odd?

  return characters[0..(digits_count/2)-1] != characters[digits_count/2..-1]
end

ranges.each do |range|
  lower_bound, upper_bound = range.split('-').map(&:strip).map(&:to_i)

  (lower_bound..upper_bound).each do |id|
    invalid_ids_total += id unless is_id_valid?(id)
  end
end

puts invalid_ids_total

