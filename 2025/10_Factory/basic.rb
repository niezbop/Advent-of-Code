input_file = ARGV[0]

class Machine
  attr_accessor :expected_lights, :buttons, :joltage_requirements

  def initialize(line)
    self.buttons = Array.new
    line.strip.split(/\s+/).each do |element|
      if element[0] == '['
        self.expected_lights = element[1..-2].chars.map {|c| c == '#'}
      elsif element[0] == '('
        self.buttons << element[1..-2].split(',').map(&:to_i)
      elsif element[0] == '{'
        self.joltage_requirements = element[1..-2].split(',').map(&:to_i) 
      else
        raise ArgumentError, "Character not valid at the beginning of #{element}"
      end
    end
  end

  def to_s
    return [
      "[#{expected_lights.map {|l| l ? '#' : '.'}.join('')}]",
      buttons.map {|b| "(#{b.join(',')})"},
      "{#{joltage_requirements.join(',')}}"
    ].flatten.join(' ')
  end
end

machines = File.readlines(input_file).map {|l| Machine.new(l) }

total = 0
machines.each do |machine|
  needed_changes = machine.expected_lights
    .each_with_index
    .map {|l,i| l ? i : nil}
    .compact.sort

  next if needed_changes.empty?
  possible_changes = machine.buttons
  presses = 1
  loop do
    break if possible_changes.any? {|c| c == needed_changes}
    combined_changes = [] 
    possible_changes.each do |change|
      machine.buttons.each do |button|
        combination = change.dup
        button.each do |i|
          if combination.include?(i)
            combination.delete(i)
          else
            combination << i
          end
        end
        combined_changes = combined_changes | [combination.sort] unless combination.empty?
      end
    end
    possible_changes = combined_changes
    presses += 1
  end
  
  total += presses
end

puts total
