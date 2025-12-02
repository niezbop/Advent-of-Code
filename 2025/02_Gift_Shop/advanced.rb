require 'prime'

input_file = ARGV[0]

input = File.read(input_file)

ranges = input.split(',')

invalid_ids_total = 0

def is_id_valid?(id)
  characters = id.to_s
  # Trivial check if all characters are the same
  digits_count = characters.length
  return true if digits_count == 1
  return false if characters.chars.uniq.size == 1
  # To get even chunks of characters, we break down the string by prime factors
  Prime.prime_division(digits_count).each do |prime, exponent|
    return true if prime == digits_count
    (1..exponent).to_a.reverse.each do |exp|
      factor = prime ** exp
      next if factor == digits_count
      chunks = []
      l,u = [0,factor-1]
      loop do
        chunks << characters[l..u]
        l += factor
        u += factor
        break if u >= digits_count
      end
      # The ID is invalid if all chunks are identical in the breakdown
      # We can interrupt the check here, we have found at least one repeatition
      return false if chunks.uniq.size == 1
    end
  end

  return true
end

ranges.each do |range|
  lower_bound, upper_bound = range.split('-').map(&:strip).map(&:to_i)

  (lower_bound..upper_bound).each do |id|
    next if is_id_valid?(id)
    invalid_ids_total += id
  end
end

puts invalid_ids_total

