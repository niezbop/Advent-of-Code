input_file = ARGV[0]

lines = File.readlines(input_file)

beams = [lines[0].index('S')]
splits = 0

lines[1..-1].each do |line|
  previous_beams = beams.dup
  previous_beams.each do |i|
    if line[i] == '^'
      beams.delete(i)
      beams << i-1 unless beams.include?(i-1)
      beams << i+1 unless beams.include?(i+1)
      splits += 1
    end
  end
end

puts splits
