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

  # A hash which indicates which voltages are activated by which buttons
  def joltage_buttons
    return self.joltage_requirements.each_with_index.map do |_, i|
      j_buttons = []
      buttons.each_with_index {|b,j| j_buttons << j if b.include?(i) }
      [i, j_buttons]
    end.to_h
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

def find_arrangement(given, expected, buttons)
  joltage_buttons = expected.size.times.map do |i|
    j_buttons = []
    buttons.each_with_index {|b,j| j_buttons << j if b.include?(i) }
    [i, j_buttons]
  end.to_h.reject {|_,b| b.empty?}

  # Pick joltage affected by the lowest amount of buttons
  lowest_complexity, joltages = joltage_buttons.group_by {|_,b| b.size}.sort_by {|s,_| s}.first
  candidates = []
  joltages.sort_by {|ji, _| expected[ji] }.each do |joltage_index, joltage_button_indices|
    missing_joltage = expected[joltage_index] - given[joltage_index]
    if lowest_complexity == 1
      button = buttons[joltage_button_indices[0]]
      candidates << [[button, missing_joltage]]
    elsif lowest_complexity == 2
      button1 = buttons[joltage_button_indices[0]]
      button2 = buttons[joltage_button_indices[1]]
      (0..missing_joltage).each do |delta|
        candidates += [[[button1, delta], [button2, missing_joltage - delta]]]
      end
    elsif lowest_complexity == 3
      button1 = buttons[joltage_button_indices[0]]
      button2 = buttons[joltage_button_indices[1]]
      button3 = buttons[joltage_button_indices[2]]
      (0..missing_joltage).each do |i|
        (0..missing_joltage-i).each do |j|
          candidates += [[
            [button1, i],
            [button2, j],
            [button3, missing_joltage - i - j]
          ]]
        end
      end
    elsif lowest_complexity == 4
      button1 = buttons[joltage_button_indices[0]]
      button2 = buttons[joltage_button_indices[1]]
      button3 = buttons[joltage_button_indices[2]]
      button4 = buttons[joltage_button_indices[3]]
      (0..missing_joltage).each do |i|
        (0..missing_joltage-i).each do |j|
          (0..missing_joltage-i-j).each do |k|
            candidates += [[
              [button1, i],
              [button2, j],
              [button3, k],
              [button4, missing_joltage-i-j-k]
            ]]
          end
        end
      end
    else
      raise StandardError, "Cannot process complexity > 3 (given complexity is #{lowest_complexity})" 
    end
  end

  possible_arrangements = []
  candidates.each do |button_pushes|
    new_state = given.dup
    remaining_buttons = buttons.dup
    candidate_presses = 0
    button_pushes.each do |button, pushes|
      button.each {|index| new_state[index] += pushes}
      candidate_presses += pushes
      remaining_buttons.delete(button)
    end
    # Check if this candidate overshoots any of the requirements
    next if new_state.each_with_index.any? {|s,i| s > expected[i]}

    if new_state == expected
      possible_arrangements << button_pushes
    elsif remaining_buttons.none?
      # We're out of buttons, and not at the correct result, this is going nowhere
      next
    else
      sub_arrangement = find_arrangement(new_state, expected, remaining_buttons)
      next if sub_arrangement.nil?
      possible_arrangements << button_pushes + sub_arrangement
    end
  end

  return nil if possible_arrangements.empty?
  return possible_arrangements.sort_by {|arr| arr.map {|_, c| c}.sum}.first
end

total = 0
machines.each_with_index do |machine, index|
  print "\r[#{index}/#{machines.count}]"
  arrangement = find_arrangement(
    machine.joltage_requirements.map { 0 },
    machine.joltage_requirements,
    machine.buttons)
  raise StandardError if arrangement.nil?
  total += arrangement.map {|_, c| c}.sum
end

puts total
