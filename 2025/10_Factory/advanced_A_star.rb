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

# A*
def find_shortest_sequence(machine)
  heuristic = Proc.new do |joltage|
    distance = 0
    joltage.each_with_index do |ji, i|
      if ji > machine.joltage_requirements[i]
        distance = Float::INFINITY # Impossible to go down
        break
      end
      distance += machine.joltage_requirements[i] - ji
    end
    distance
  end

  start_joltage = machine.joltage_requirements.map {|_| 0}
  open_set = [start_joltage]

  parents = Hash.new

  g_score = Hash.new {|h,k| h[k] = Float::INFINITY }
  g_score[start_joltage] = 0

  f_score = Hash.new {|h,k| h[k] = Float::INFINITY }
  f_score[start_joltage] = heuristic.call(start_joltage)

  puts machine.joltage_requirements.inspect

  until open_set.empty? do
    current = open_set.sort_by {|j| f_score[j]}.first

    print "\r#{current.inspect}"
    if current == machine.joltage_requirements
      # Do something cool
      return g_score[current]
    end

    open_set.delete(current)
    machine.buttons.each do |button|
      [100, 50, 10, 1].each do |step|
        new_joltage = current.dup
        button.each {|i| new_joltage[i] += step }
        tentative_g_score = g_score[current] + step
        if tentative_g_score < g_score[new_joltage]
          parents[new_joltage] = current
          g_score[new_joltage] = tentative_g_score
          f_score[new_joltage] = tentative_g_score + heuristic.call(new_joltage)
          open_set = open_set | [new_joltage]
        end
      end
    end
  end

  raise StandardError, "No sequence found"
end

total = 0
machines.each do |machine|
  puts machine
  total += find_shortest_sequence(machine)
  break
end

puts total
