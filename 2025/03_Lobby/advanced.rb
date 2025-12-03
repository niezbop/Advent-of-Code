input_file = ARGV[0]

banks = File.readlines(input_file)

total = 0

def find_highest_value(batteries, digit_count, start_index = 0)
  exponent = digit_count - 1

  max = -1
  batteries[start_index..-digit_count].each_with_index do |digit, index|
    digit_value = (10**exponent) * digit
    sub_value = digit_count == 1 ? 0 :
      find_highest_value(batteries, digit_count - 1, index+1)
    value = digit_value + sub_value
    max = value if max < value
  end

  return max
end

banks.each do |bank|
  batteries = bank.strip.chars.map(&:to_i)
  
  bank_max = find_highest_value(batteries, 2)

  total += bank_max
end

puts total
