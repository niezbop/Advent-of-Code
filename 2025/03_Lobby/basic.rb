input_file = ARGV[0]

banks = File.readlines(input_file)

total = 0

banks.each do |bank|
  batteries = bank.strip.chars.map(&:to_i)
  
  bank_max = -1
  batteries[0..-2].each_with_index do |first, index|
    batteries[index+1..-1].each do |second|
      value = 10 * first + second
      bank_max = value if bank_max < value
    end
  end

  total += bank_max
end

puts total
