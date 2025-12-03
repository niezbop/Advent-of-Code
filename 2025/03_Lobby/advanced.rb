input_file = ARGV[0]

banks = File.readlines(input_file)

total = 0

def find_highest_value(batteries, digit_count, start_index = 0)
  highest_digit = batteries[start_index..-digit_count].max
  
  return highest_digit if digit_count == 1

  factor = 10 ** (digit_count - 1)
  new_index = batteries[start_index..-digit_count].index(highest_digit) + start_index + 1
  return highest_digit * factor + find_highest_value(batteries, digit_count - 1, new_index)
end

banks.each do |bank|
  batteries = bank.strip.chars.map(&:to_i)
  
  bank_max = find_highest_value(batteries, 12)

  total += bank_max
end

puts total
